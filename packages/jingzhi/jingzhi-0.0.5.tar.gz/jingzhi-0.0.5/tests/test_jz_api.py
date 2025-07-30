from jingzhi.jz_api import JzApi

def test_jz_pt():
    jz = JzApi()

    jzapi = JzApi()

    # models = jzapi.list_models("trending", 1, 1)

    
    # datasets = jzapi.list_datasets("trending", 1, 1)
    # # print(models)
    # print(datasets)

    # test = jzapi.model_info("ww/test_model")
    # print(test)

    exist = jzapi.repo_exists("ww/test_model", "model")
    print(exist)


    # files = jzapi.file_exists("ww/test_model", "model", "main", "README.md")
    # print(files)

    # files = jzapi.list_files("ww/test_model", "model", "main")
    # print(files.content)

test_jz_pt()