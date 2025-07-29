import asyncio
import json
import jsonpickle
import logging
from typing import Callable, List, Optional

from mcp import ClientSession, types
from google.adk.tools.mcp_tool import MCPTool, MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import MCPSessionManager

from ..utils import get_logger
logger = get_logger(__name__)


async def logging_handler(
    params: types.LoggingMessageNotificationParams,
) -> None:
    logger.log(getattr(logging, params.level.upper()), params.data)


class MCPSessionManagerWithLoggingCallback(MCPSessionManager):
    def __init__(
      self,
      logging_callback=None,
      **kwargs,
    ):
        super().__init__(**kwargs)
        self.logging_callback = logging_callback

    async def create_session(self) -> ClientSession:
        session = await super().create_session()
        session._logging_callback = self.logging_callback
        return session


class CalculationMCPTool(MCPTool):
    def __init__(
        self,
        executor: Optional[dict] = None,
        storage: Optional[dict] = None,
        async_mode: bool = False,
        wait: bool = True,
        submit_tool: Optional[MCPTool] = None,
        query_tool: Optional[MCPTool] = None,
        terminate_tool: Optional[MCPTool] = None,
        results_tool: Optional[MCPTool] = None,
        query_interval: int = 10,
        logging_callback: Callable = logging_handler,
    ):
        """Calculation MCP tool
        extended from google.adk.tools.mcp_tool.MCPTool

        Args:
            executor: The executor configuration of the calculation tool.
                It is a dict where the "type" field specifies the executor
                type, and other fields are the keyword arguments of the
                corresponding executor type.
            storage: The storage configuration for storing artifacts. It is
                a dict where the "type" field specifies the storage type,
                and other fields are the keyword arguments of the
                corresponding storage type.
            async_mode: Submit and query until the job finishes, instead of
                waiting in single connection
            wait: Wait for the job to finish or directly return
            submit_tool: The tool of submitting job
            query_tool: The tool of querying job status
            terminate_tool: The tool of terminating job
            results_tool: The tool of getting job results
            query_interval: Time interval of querying job status
            logging_callback: Callback function for server notifications
        """
        self.executor = executor
        self.storage = storage
        self.async_mode = async_mode
        self.submit_tool = submit_tool
        self.query_tool = query_tool
        self.terminate_tool = terminate_tool
        self.results_tool = results_tool
        self.query_interval = query_interval
        self.wait = wait
        self.logging_callback = logging_callback

    async def log(self, level, message):
        await self.logging_callback(types.LoggingMessageNotificationParams(
            data=message, level=level.lower()))

    async def run_async(self, args, **kwargs):
        if "executor" not in args:
            args["executor"] = self.executor
        if "storage" not in args:
            args["storage"] = self.storage
        if not self.async_mode:
            return await super().run_async(args=args, **kwargs)

        executor = args["executor"]
        storage = args["storage"]
        res = await self.submit_tool.run_async(args=args, **kwargs)
        if res.isError:
            logger.error(res.content[0].text)
            return res
        job_id = json.loads(res.content[0].text)["job_id"]
        job_info = res.content[0].job_info
        await self.log("info", "Job submitted (ID: %s)" % job_id)
        if job_info.get("extra_info"):
            await self.log("info", job_info["extra_info"])
            if not self.wait:
                return job_info['extra_info']

        while True:
            res = await self.query_tool.run_async(
                args={"job_id": job_id, "executor": executor}, **kwargs)
            if res.isError:
                logger.error(res.content[0].text)
            else:
                status = res.content[0].text
                await self.log("info", "Job %s status is %s" % (
                    job_id, status))
                if status != "Running":
                    break
            await asyncio.sleep(self.query_interval)

        res = await self.results_tool.run_async(
            args={"job_id": job_id, "executor": executor, "storage": storage},
            **kwargs)
        if res.isError:
            await self.log("error", "Job %s failed: %s" % (
                job_id, res.content[0].text))
        else:
            await self.log("info", "Job %s result is %s" % (
                job_id, jsonpickle.loads(res.content[0].text)))
        res.content[0].job_info = {**job_info,
                                   **getattr(res.content[0], "job_info", {})}
        return res


class CalculationMCPToolset(MCPToolset):
    def __init__(
        self,
        executor: Optional[dict] = None,
        storage: Optional[dict] = None,
        executor_map: Optional[dict] = None,
        async_mode: bool = False,
        wait: bool = True,
        logging_callback: Callable = logging_handler,
        **kwargs,
    ):
        """
        Calculation MCP toolset

        Args:
            executor: The default executor configuration of the calculation
                tools. It is a dict where the "type" field specifies the
                executor type, and other fields are the keyword arguments of
                the corresponding executor type.
            storage: The storage configuration for storing artifacts. It is
                a dict where the "type" field specifies the storage type,
                and other fields are the keyword arguments of the
                corresponding storage type.
            executor_map: A dict mapping from tool name to executor
                configuration for specifying particular executor for certain
                tools
            async_mode: Submit and query until the job finishes, instead of
                waiting in single connection
            logging_callback: Callback function for server notifications
        """
        super().__init__(**kwargs)
        self.logging_callback = logging_callback
        self._mcp_session_manager = MCPSessionManagerWithLoggingCallback(
            connection_params=self._connection_params,
            errlog=self._errlog,
            logging_callback=logging_callback,
        )
        self.executor = executor
        self.storage = storage
        self.wait = wait
        self.executor_map = executor_map or {}
        self.async_mode = async_mode

    async def get_tools(self, *args, **kwargs) -> List[CalculationMCPTool]:
        tools = await super().get_tools(*args, **kwargs)
        tools = {tool.name: tool for tool in tools}
        calc_tools = []
        for tool in tools.values():
            if tool.name.startswith("submit_") or tool.name in [
                    "query_job_status", "terminate_job", "get_job_results"]:
                continue
            calc_tool = CalculationMCPTool(
                executor=self.executor_map.get(tool.name, self.executor),
                storage=self.storage,
                async_mode=self.async_mode,
                wait=self.wait,
                submit_tool=tools.get("submit_" + tool.name),
                query_tool=tools.get("query_job_status"),
                terminate_tool=tools.get("terminate_job"),
                results_tool=tools.get("get_job_results"),
                logging_callback=self.logging_callback,
            )
            calc_tool.__dict__.update(tool.__dict__)
            calc_tools.append(calc_tool)
        return calc_tools
