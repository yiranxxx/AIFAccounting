CREATE TABLE CommissionInfo (
    CommissionID VARCHAR(255) PRIMARY KEY NOT NULL,
    InstitutionName VARCHAR(255) NOT NULL,
    ReportStartDate DATE NOT NULL,
    ReportEndDate DATE NOT NULL,
    FileNumber VARCHAR(255) NOT NULL,
    AdvisorCode VARCHAR(255) NOT NULL,
    AdvisorName VARCHAR(255) NOT NULL,
    ContractDate DATE NOT NULL,
    ContractStatus VARCHAR(255) NOT NULL,
    Agency VARCHAR(255) NOT NULL,
    District VARCHAR(255) NOT NULL,
    TimeStamp DATETIME NOT NULL  DEFAULT getdate()
);

CREATE TABLE CommissionPayment (
    CommissionPaymentID INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    CommissionID VARCHAR(255) NOT NULL,
    CompanyCode VARCHAR(255) NOT NULL,
    PayToName VARCHAR(255) NOT NULL,
    TransactionDate DATE NOT NULL,
    TransactionType VARCHAR(255) NOT NULL,
    CommPer FLOAT NOT NULL,
    AmountDue MONEY NOT NULL,
    Balance MONEY NOT NULL,
    CurrentBalance MONEY NOT NULL,
    TimeStamp DATETIME NOT NULL DEFAULT getdate()

    CONSTRAINT FK_CommissionPayment_CommissionID
        FOREIGN KEY (CommissionID) REFERENCES CommissionInfo(CommissionID)
);

CREATE TABLE CommissionDetail (
    CommissionDetailID INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    CommissionID VARCHAR(255) NOT NULL,
    CustomerName VARCHAR(255) NOT NULL,
    ContractNumber VARCHAR(255) NULL,
    CoverageName VARCHAR(255) NULL,
    TransactionDate DATE NULL,
    TransactionType VARCHAR(255) NULL,
    CompensationBasisAmount MONEY NULL,
    RPLPer FLOAT NULL,
    SharPer FLOAT NULL,
    CommPer FLOAT NULL,
    AmountDue MONEY NULL,
    Balance MONEY NULL,
    CommissionType VARCHAR(255) NOT NULL,
	TimeStamp DATETIME NOT NULL DEFAULT getdate()

	CONSTRAINT FK_CommissionDetail_CommissionID 
		FOREIGN KEY (CommissionID) REFERENCES CommissionInfo(CommissionID)
);

