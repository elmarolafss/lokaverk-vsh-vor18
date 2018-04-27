### Users:
* id - int primary key incrementing not null
* userName - varchar(255)
* userEmail - varchar(255)
* password - varchar(100)(Hashed-MD5 or SHA1)
* date - DATE

### Product:
* id - int primary key incrementing not null
* name - varchar(255) primary key
* displayName - varchar(255)
* type - varchar(255)
* price - float
* discount - float
* colors - varchar(255)
* sizes - varchar(255)
* info - varchar(255)

### Purchase:
* id - int primary key incrementing not null
* prodId - int foreign key = Product.id
* cartId - int foreign key = Cart.id
* price - float -- tekið frá product við sölu
* discount - float -- tekið frá product við sölu
* color - varchar(255) -- tekið frá product við sölu
* size - varchar(255) -- tekið frá product við sölu
* date - DATE

### Cart:
* id - int primary key incrementing not null
* userId - int foreign key = Users.id
* totalPreTax - float
* tax - float
* discount - float
* total - float
* date - DATE
