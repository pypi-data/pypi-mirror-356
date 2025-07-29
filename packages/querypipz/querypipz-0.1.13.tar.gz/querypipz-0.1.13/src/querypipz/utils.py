""" useful tools """
from llama_index.core.workflow import Context
from llama_index.core.tools import QueryEngineTool
from llama_index.core.tools import FunctionTool

class VisualIndex():
    """visualization Index
    """
    def __init__(self,index):
        self.index = index

    def get_docs_id(self):
        """ get docs ids """
        return list(self.index.docstore.docs.keys())

    def get_documents(self):
        """ get documents """
        return [self.index.docstore.get_document(i) for i in self.get_docs_id()]

    def get_document_by_id(self,doc_id): # 有a功能
        """ get documents by doc_id """
        return self.index.docstore.get_document(doc_id)


class Package():
    """包装工具
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def package_tool(func):
        """ 包装工具 """
        return FunctionTool.from_defaults(func,name=func.__name__)

    @staticmethod
    def package_querypip2tool(query_engine,name,description):
        """ 将query包装成工具 """
        qenginetools = QueryEngineTool.from_defaults(
                query_engine=query_engine,
                name=name,
                description=description,
            )
        return qenginetools


class EasyAgentz():
    """ agent helper"""
    def __init__(self, agent):
        self.agent = agent
        self.ctx = Context(agent)
        self.resp = None

    async def run(self,prompt = "What is 5+3+2"):
        """ 
        运行agent
        """
        self.resp = await self.agent.run(prompt,ctx=self.ctx)
        return str(self.resp)

    def update_prompts(self,react_system_prompt:str):
        """ 更新prompt
        """
        self.agent.update_prompts({"react_header": react_system_prompt})

    def tool_calls(self):
        """ 查询工具调用情况"""
        return self.resp.tool_calls

class EasyIndex():
    """ Index helper"""
    def __init__(self,index):
        """ init """
        self.index = index

    def insert(self,document):
        """ 插入 document """
        self.index.insert(document)
