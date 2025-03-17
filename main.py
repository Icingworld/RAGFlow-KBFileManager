from manager.wwmanager import Manager
from config import *

if __name__ == "__main__":
    manager = Manager(
        FILE_SYSTEM_ROOT,
        FILE_SYSTEM_SUFFIX,
        RAGFLOW_URL,
        RAGFLOW_AUTHORIZATION,
        RAGFLOW_KNOWLEDGE_BASE_ID
    )
    manager.run()
