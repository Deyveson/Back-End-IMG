import pymongo

# Criando uma Conexão com o Banco de dados NoSQL (Não relacional)
# Fazendo o INSERT, SELECT, DELETE e UPDATE, buscas padronizadas (query)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# Link do MongoClient

mydb = myclient["mydatabase"]
# Meu Banco de Dados

mycol = mydb["cliente"]
# Coluna do banco


# mydict = {"name": "Thalisson", "address": "Afeganistão"}
# x = mycol.insert_one(mydict)
# #  # Fazendo um Insert no banco


myquery = {"name": 'Thalisson'}
# Fazendo uma Query


# mydoc = mycol.find({"name": "Thalisson"});


# mycol.delete_one({"address": "Afeganistão"})
# Delete apartir da Query, deleta de 1 em 1


# mycol.delete_many(myquery)
# Deleta todos que vem na querry


mydoc = mycol.find()
# Listando todos o dados do banco.


for x in mydoc:
    print(x)
# Listando os dados apartir da query.


# print(myclient.list_database_names())
# # Listando os bancos


# dblist = myclient.list_database_names()
# if "mydatabase" in dblist:
#   print("O banco de dados existe.")
# Verificando se banco existe


# for x in mycol.find({},{ "_id": 0, "name": 1, "address": 1 }):
#   print(x)
# Mostrando apenas as name e address



# myquery = {"name": "Lulu"}
# # Query pra achar o que quero editar
#
# newvalues = {"$set": {"address": "BRASIL"}}
# # Novo valor a ser inserido
#
# mycol.update_one(myquery, newvalues)
# # update
#
# for x in mycol.find():
#   print(x)
# # Listando novamente