import configparser


api_id = input('Enter api id: ')
api_hash = input('Enter api hash: ')

def createConfig(path):
    config = configparser.ConfigParser()
    config.add_section("pyrogram")
    config.set("pyrogram", "api_id", api_id)
    config.set("pyrogram", "api_hash", api_hash)

    with open(path, "w") as config_file:
        config.write(config_file)
 
 
if __name__ == "__main__":
    path = "../config.ini"
    createConfig(path)
