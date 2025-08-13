# Available Funds
# Current P&L
# Calculate Expenses
# Available Position (Number of stocks for a symbol from the available funds)

class FinLib: 
    def Expenses(self, InQTY, BuyPrice, OutQTY = 0, SalePrice=0):
        BuyAmount = InQTY * BuyPrice
        SaleAmount = OutQTY * SalePrice
        STT = 0

        #Buy
        STT = BuyAmount * 0.00025
        SEBI = BuyAmount * 0.000002
        NSE = BuyAmount * 0.0000325
        STAMP = BuyAmount * 0.00003
        BROKERAGE = BuyAmount * 0.0003
        if BROKERAGE>= 20:
            BROKERAGE = 20
        GST = BROKERAGE * 0.18

        
        BuyExpenses = SEBI+NSE+STAMP+BROKERAGE+GST
                             
        #Sale
        if SalePrice>0:
            STT = SaleAmount * 0.00025
            SEBI = SaleAmount * 0.000002
            NSE = SaleAmount * 0.0000325
            STAMP = SaleAmount * 0.00003
            BROKERAGE = SaleAmount * 0.0003
            if BROKERAGE>= 20:
                BROKERAGE = 20
            GST = BROKERAGE * 0.18
            SaleExpenses = STT + (SEBI+NSE+STAMP+BROKERAGE+GST)
            Total_Expenses = BuyExpenses + SaleExpenses
        else:
            Total_Expenses = STT + ((BuyExpenses)*2)
        return Total_Expenses


    def PnLWithExpenses(self, InQTY, OutQTY, BuyPrice, SalePrice):
        Amount = (SalePrice*OutQTY) - ((BuyPrice*InQTY) + self.Expenses(InQTY, BuyPrice, OutQTY, SalePrice))
        return Amount
        
    def AveragePrice(self, PreviousQty, PreviousPrice, NewQty, NewPrice):
        AvgPrice = (((PreviousQty*PreviousPrice) + (NewQty*NewPrice))/(PreviousQty+NewQty))
        return AvgPrice

        

