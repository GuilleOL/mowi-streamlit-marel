from sql_engine import sql_engine
import timeit

print("creando engine")
sql =  sql_engine("conf.yml")

print("Realizando query")
df = sql.query_table(2)#,fromd='2022-02-08')

print("Guardando feather")
df.to_feather( "bateas.feather" )

print("Mostrando feather")
print(df)
                    
print("Realizando query")
df = sql.query_table(3)#,fromd='2022-02-08')

print("Guardando feather")
df.to_feather( "consumos.feather" )

print("Mostrando feather")
print(df)
                    
print("Realizando query")
df = sql.query_table(0)#,fromd='2022-02-08')

print("Guardando feather")
df.to_feather( "piezas.feather" )

print("Mostrando feather")
print(df)