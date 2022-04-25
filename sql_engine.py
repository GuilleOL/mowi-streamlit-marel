import sqlalchemy, yaml
import pandas as pd

class sql_engine:
    def __init__(self,fname) -> None:
        super().__init__()
        self.fname = fname
        self.read_yaml(fname)
        self.engine = self.createengine()

    def createengine(self):
        """
        Usa diccionario con información de servidor sql para crear 
        engine de sql.
        Returns
        -------
        Object
            Objeto para leer sql
        """
        creds = self.read_yaml(self.fname)
        engine_path = 'mssql+pymssql://{}:{}@{}/{}'
        # TODO: que tire error si las credenciales están malas
        return sqlalchemy.create_engine(
            engine_path.format(creds['db']['username'],
                            creds['db']['password'], creds['db']['host'],
                            creds['db']['database']))
        #dict_data = self.read_yaml(self.fname)

    @staticmethod
    def read_yaml(fname:str):
        """
        Lee arhivos tipo yaml (.yml) y retorna diccionario con parametros.
        Parameters
        ----------
        f : string
            Filename del archivo yaml.
        Returns
        -------
        dict
            Diccionario con parametros.
        """
        return yaml.load(open(fname, 'r'), Loader=yaml.FullLoader)
    
    def query(self, query, _print=False):
        """
        Hace una query en el motor de base datos anteriormente registrado
        Parameters
        ----------
        qry : string
            Query a la base de datos.
        engine : sql.object
            Objecto Engine.
        Returns
        -------
        df : pandas.dataframe
            Dataframe con la respuesta de la consulta.
        """
        if _print:
            print("Querying...")
            print("\n" + query + "\n")
            df = pd.read_sql_query(query, self.engine)
            print("Query completed.")
        else:
            df = pd.read_sql_query(query, self.engine)    
        return df

    def query_table(self, table=None, fromd= '2000-01-01' , tod= '2100-01-01' ,_print=False):
        """
        Hace una query en el motor de base datos anteriormente registrado
        Parameters
        ----------
        qry : string
            Query a la base de datos.
        engine : sql.object
            Objecto Engine.
        Returns
        -------
        df : pandas.dataframe
            Dataframe con la respuesta de la consulta.
        """
        if type(table) is int:
            table = ["vAlaya_recepcion",
                     "vAlaya_produccion",
                     "vAlaya_bateas",
                     "vAlaya_consumos"][table]
        if table == "vAlaya_recepcion":
            str_date = "AlaImpPiezaWfeFechaHora"
        if table == "vAlaya_produccion":
            str_date = "AlaImpPackFechaHora"
        if table == "vAlaya_bateas":
            str_date = "AlaImpBatFecDesp"
        if table == "vAlaya_consumos":
            str_date = "AlaImpConFecHorReg"
            
        query = """ SELECT *
                FROM [IRPM].[dbo].[{}]
                WHERE [{}] >= '{}' and 
                    [{}] <= '{}' """.format(table,
                                            str_date,
                                            fromd,
                                            str_date,
                                            tod)
        if _print:
            print("Querying...")
            print("\n" + query + "\n")
            df = pd.read_sql_query(query, self.engine)
            print("Query completed.")
        else:
            df = pd.read_sql_query(query, self.engine)    
        return df

