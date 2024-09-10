import environs

env = environs.Env()
env.read_env("./.env")

api_id = 28101483 env.int("API_ID")
api_hash = "89c6f91a0bcf78bb5ae7cf67b3734f82" env.str("API_HASH")

db_type = env.str("DATABASE_TYPE")
db_url = env.str("DATABASE_URL", "")
db_name = env.str("DATABASE_NAME")

test_server = env.bool("TEST_SERVER", False)
modules_repo_branch = env.str("MODULES_REPO_BRANCH", "master")
