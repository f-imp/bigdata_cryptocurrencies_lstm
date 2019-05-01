-- international bitcoin currency information 
DROP TABLE IF EXISTS "currency_info";
CREATE TABLE "currency_info"(
    currency_code	VARCHAR (10),
    currency 		TEXT
);

DROP TABLE IF EXISTS "btc_prices";
CREATE TABLE "btc_prices"(
    time            TIMESTAMP WITH TIME ZONE NOT NULL,
    opening_price   DOUBLE PRECISION,
    highest_price   DOUBLE PRECISION,
    lowest_price    DOUBLE PRECISION,
    closing_price   DOUBLE PRECISION,
    volume_btc      DOUBLE PRECISION,
    volume_currency DOUBLE PRECISION,
    currency_code   VARCHAR (10)
);

DROP TABLE IF EXISTS "crypto_prices";
CREATE TABLE "crypto_prices"(
    time            TIMESTAMP WITH TIME ZONE NOT NULL,
    opening_price   DOUBLE PRECISION,
    highest_price   DOUBLE PRECISION,
    lowest_price    DOUBLE PRECISION,
    closing_price   DOUBLE PRECISION,
    volume_crypto   DOUBLE PRECISION,
    volume_btc      DOUBLE PRECISION,
    currency_code   VARCHAR (10)
);

SELECT create_hypertable('btc_prices', 'time', 'opening_price', 2);
SELECT create_hypertable('crypto_prices', 'time', 'currency_code', 2);