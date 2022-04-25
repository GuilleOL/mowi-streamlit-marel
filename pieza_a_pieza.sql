
SELECT [AlaImpPiezaWfeId]

      ,[AlaImpPiezaWfePlanta]

      ,[AlaImpPiezaWfeLote]

      ,[AlaImpPiezaWfeCentro]

      ,[AlaImpPiezaWfePesoNeto]

      ,[AlaImpPiezaWfeFechaHora]

      ,[AlaImpPiezaWfeJaula]

      ,[AlaImpPiezaWfeGate]

  FROM [IRPM].[dbo].[vAlaya_recepcion]
  WHERE [AlaImpPiezaWfeFechaHora] >= '2020-01-01' and [AlaImpPiezaWfeFechaHora] <= '2021-01-01' 