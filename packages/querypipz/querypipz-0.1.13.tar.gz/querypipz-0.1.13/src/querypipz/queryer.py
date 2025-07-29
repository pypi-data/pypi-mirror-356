""" queryer.py """
import os
from contextlib import contextmanager
from llama_index.core import (
    load_index_from_storage,
    StorageContext,
    VectorStoreIndex,
    PropertyGraphIndex,
    Document,
)
from llama_index.core import SimpleKeywordTableIndex
from querypipz.abc_ import QueryerABC

@contextmanager
def safe_operation(info:str):
    """ try catch"""
    try:
        yield
    except Exception as e:
        # raise TypeError(info +f": {e}")
        raise TypeError(info) from e

class Queryer(QueryerABC):
    """query类

    Args:
        QueryerABC (_type_): _description_
    """
    def __init__(self):
        super().__init__()
        self.persist_path = None
        self.reader = None
        self.ingestion_pipeline = None
        self.kg_extractors = None
        self.storage_context = None
        self.index_type = None
        self.retriever_nest = None
        self.query_nest = None
        self.query_pipeline = None
        self.retriever = None
        self.index = None

    def build(self,cover = False):
        # 初始化文件夹/文件
        if os.path.exists(self.persist_path) and cover is False:
            return 'index exists, you can build force with cover set True'

        # 初始化Reader
        with safe_operation("Reader"):
            if self.reader is None :
                documents = []
            else:
                documents = self.reader.load_data(show_progress = True)

        chunk_size = 10
        for i in range(len(documents)// chunk_size + 1):
            documents_chunk = documents[i*chunk_size:(i+1)*chunk_size]
            nodes = None
            print(f'chunk: {i}')
            print(documents_chunk,'documents_chunk')#  [] or [Document , Document]

            with safe_operation("Ingestion"):
                if self.ingestion_pipeline:
                    nodes = self.ingestion_pipeline.run(documents=documents_chunk,
                                                        show_progress = True)


            with safe_operation("Index"):
                if self.index_type == "VectorStoreIndex":
                    if nodes:
                        self.index = VectorStoreIndex(
                                    nodes,
                                    storage_context = self.storage_context,
                                    show_progress=True,
                                                        )
                    else:
                        self.index = VectorStoreIndex.from_documents(
                                    documents_chunk,
                                    storage_context = self.storage_context,
                                    show_progress=True,
                        )
                elif self.index_type == "SimpleKeywordTableIndex":
                    if nodes:
                        self.index = SimpleKeywordTableIndex(
                                    nodes,
                                    storage_context = self.storage_context,
                                    show_progress=True,
                                                        )
                    else:
                        self.index = SimpleKeywordTableIndex.from_documents(
                                    documents_chunk,
                                    storage_context = self.storage_context,
                                    show_progress=True,
                                    )
                elif self.index_type == "PropertyGraphIndex":
                    if nodes:
                        self.index = PropertyGraphIndex(
                                    nodes,
                                    kg_extractors = self.kg_extractors,
                                    storage_context = self.storage_context,
                                    show_progress=True,
                                                        )
                    else:
                        self.index = PropertyGraphIndex.from_documents(
                                    documents_chunk,
                                    kg_extractors = self.kg_extractors,
                                    storage_context = self.storage_context,
                                    show_progress=True,
                                    )

            with safe_operation("Storage"):
                self.index.storage_context.persist(self.persist_path)

        return 'builded'

    def load(self):
        """_summary_
        """
        assert 1==1
        storage_context = StorageContext.from_defaults(persist_dir=self.persist_path)
        self.index = load_index_from_storage(storage_context=storage_context)

    def reload(self):
        """ reload """
        self.retriever = None

    def update(self, prompt: str):
        if not os.path.exists(self.persist_path):
            os.makedirs(self.persist_path)
        else:
            self.load()
        documents = [Document(text = prompt)]
        if self.ingestion_pipeline:
            nodes = self.ingestion_pipeline.run(documents=documents,show_progress = True)
            self.index.insert_nodes(nodes)
        else:
            self.index.insert(documents[0])
        self.index.storage_context.persist(self.persist_path)

    def query(self, prompt: str, similarity_top_k: int = 3):
        """
        执行查询。
        """
        query_engine = self._get_query_engine(similarity_top_k=similarity_top_k)
        return query_engine.query(prompt)

    def retrieve_search(self, query_text: str, similarity_top_k: int = 5):
        """
        使用检索器进行检索。
        """
        retriever = self._get_retriever(similarity_top_k=similarity_top_k)
        return retriever.retrieve(query_text)

    def _get_retriever(self, similarity_top_k: int = 5):
        """
        获取检索器（Retriever），如有必要则从持久化目录加载索引。
        """
        if self.retriever is not None:
            return self.retriever

        if not self.persist_path or not os.path.exists(self.persist_path):
            raise ValueError("索引持久化目录不存在，无法构建检索器。")

        if self.retriever_nest is None:
            storage_context = StorageContext.from_defaults(persist_dir=self.persist_path)
            self.index = load_index_from_storage(storage_context=storage_context)
            self.retriever = self.index.as_retriever(similarity_top_k=similarity_top_k,
                                                    include_text=False,
                                                    )
            return self.retriever
        else:
            storage_context = StorageContext.from_defaults(persist_dir=self.persist_path)
            self.index = load_index_from_storage(storage_context=storage_context)
            self.retriever_nest.complex_build(index = self.index)
            self.retriever = self.retriever_nest
            return self.retriever

    def _get_query_engine(self, similarity_top_k: int = 3):
        """
        获取查询引擎（QueryEngine），如有必要则从持久化目录加载索引。
        """
        if self.query_pipeline is not None:
            return self.query_pipeline


        if not self.persist_path or not os.path.exists(self.persist_path):
            raise ValueError("索引持久化目录不存在，无法构建查询引擎。")

        if self.retriever_nest is None and self.query_nest is None:
            storage_context = StorageContext.from_defaults(persist_dir=self.persist_path)
            self.index = load_index_from_storage(storage_context=storage_context)
            self.query_pipeline = self.index.as_query_engine(similarity_top_k=similarity_top_k,
                                                        include_text=True,)
            return self.query_pipeline
        else:
            pass
