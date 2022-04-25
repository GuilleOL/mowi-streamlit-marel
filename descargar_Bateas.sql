SELECT [AlaImpBateaId]
    
      ,[AlaImpBatPlanta]

      ,[AlaImpBatNro]

      ,[AlaImpBatGuia]

      ,[AlaImpBatEspecie]

      ,[AlaImpBatPiezas]

      ,[AlaImpBatKilos]

      ,[AlaImpBatDG]

      ,[AlaImpBatCentro]

      ,[AlaImpBatJaula]

      ,[AlaImpBatFecDesp]

      ,[AlaImpBatEstado]

      ,[AlaImpBatIniDescarga]

      ,[AlaImpBatPermanencia]

  FROM [IRPM].[dbo].[vAlaya_bateas]
  WHERE [AlaImpBatFecDesp] >= '2022-01-01' and [AlaImpBatFecDesp] <= '2023-01-01' 