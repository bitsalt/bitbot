import Forex.config as fxconfig

class Account:

    def __init__(self):
        cfg = fxconfig.make_config_instance()
        api = cfg.create_context()
        response = api.account.summary(cfg.active_account)
        account = response.body['account']

        self.id = account.id

        #
        # Client-assigned alias for the Account. Only provided if the Account
        # has an alias set
        #
        self.alias = account.alias

        #
        # The home currency of the Account
        #
        self.currency = account.currency

        #
        # The current balance of the Account.
        #
        self.balance = account.balance

        #
        # ID of the user that created the Account.
        #
        self.createdByUserID = account.createdByUserID

        #
        # The date/time when the Account was created.
        #
        self.createdTime = account.createdTime

        #
        # The current guaranteed Stop Loss Order mode of the Account.
        #
        self.guaranteedStopLossOrderMode = account.guaranteedStopLossOrderMode

        #
        # The total profit/loss realized over the lifetime of the Account.
        #
        self.pl = account.pl

        #
        # The total realized profit/loss for the Account since it was last
        # reset by the client.
        #
        self.resettablePL = account.resettablePL

        #
        # The date/time that the Account's resettablePL was last reset.
        #
        self.resettablePLTime = account.resettablePLTime

        #
        # The total amount of financing paid/collected over the lifetime of the
        # Account.
        #
        self.financing = account.financing

        #
        # The total amount of commission paid over the lifetime of the Account.
        #
        self.commission = account.commission

        #
        # The total amount of fees charged over the lifetime of the Account for
        # the execution of guaranteed Stop Loss Orders.
        #
        self.guaranteedExecutionFees = account.guaranteedExecutionFees

        #
        # Client-provided margin rate override for the Account. The effective
        # margin rate of the Account is the lesser of this value and the OANDA
        # margin rate for the Account's division. This value is only provided
        # if a margin rate override exists for the Account.
        #
        self.marginRate = account.marginRate

        #
        # The date/time when the Account entered a margin call state. Only
        # provided if the Account is in a margin call.
        #
        self.marginCallEnterTime = account.marginCallEnterTime

        #
        # The number of times that the Account's current margin call was
        # extended.
        #
        self.marginCallExtensionCount = account.marginCallExtensionCount

        #
        # The date/time of the Account's last margin call extension.
        #
        self.lastMarginCallExtensionTime = account.lastMarginCallExtensionTime

        #
        # The number of Trades currently open in the Account.
        #
        self.openTradeCount = account.openTradeCount

        #
        # The number of Positions currently open in the Account.
        #
        self.openPositionCount = account.openPositionCount

        #
        # The number of Orders currently pending in the Account.
        #
        self.pendingOrderCount = account.pendingOrderCount

        #
        # Flag indicating that the Account has hedging enabled.
        #
        self.hedgingEnabled = account.hedgingEnabled

        #
        # The date/time of the last order that was filled for this account.
        #
        self.lastOrderFillTimestamp = account.lastOrderFillTimestamp

        #
        # The total unrealized profit/loss for all Trades currently open in the
        # Account.
        #
        self.unrealizedPL = account.unrealizedPL

        #
        # The net asset value of the Account. Equal to Account balance +
        # unrealizedPL.
        #
        self.NAV = account.NAV

        #
        # Margin currently used for the Account.
        #
        self.marginUsed = account.marginUsed

        #
        # Margin available for Account currency.
        #
        self.marginAvailable = account.marginAvailable

        #
        # The value of the Account's open positions represented in the
        # Account's home currency.
        #
        self.positionValue = account.positionValue

        #
        # The Account's margin closeout unrealized PL.
        #
        self.marginCloseoutUnrealizedPL = account.marginCloseoutUnrealizedPL

        #
        # The Account's margin closeout NAV.
        #
        self.marginCloseoutNAV = account.marginCloseoutNAV

        #
        # The Account's margin closeout margin used.
        #
        self.marginCloseoutMarginUsed = account.marginCloseoutMarginUsed

        #
        # The Account's margin closeout percentage. When this value is 1.0 or
        # above the Account is in a margin closeout situation.
        #
        self.marginCloseoutPercent = account.marginCloseoutPercent

        #
        # The value of the Account's open positions as used for margin closeout
        # calculations represented in the Account's home currency.
        #
        self.marginCloseoutPositionValue = account.marginCloseoutPositionValue

        #
        # The current WithdrawalLimit for the account which will be zero or a
        # positive value indicating how much can be withdrawn from the account.
        #
        self.withdrawalLimit = account.withdrawalLimit

        #
        # The Account's margin call margin used.
        #
        self.marginCallMarginUsed = account.marginCallMarginUsed

        #
        # The Account's margin call percentage. When this value is 1.0 or above
        # the Account is in a margin call situation.
        #
        self.marginCallPercent = account.marginCallPercent

        #
        # The ID of the last Transaction created for the Account.
        #
        self.lastTransactionID = account.lastTransactionID

    def get_account_info(self, key):
        if key == 'currency':
            return self.account.currency
