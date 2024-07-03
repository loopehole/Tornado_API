# chmod +x test_guardarian_endpoints.sh -> make this script executable
# ./test_guardarian_endpoints.sh -> for executing this script
#!/bin/bash

API_KEY="010cb33d-a368-4e4e-bf59-cfbc44ffcb66"
SECRET_KEY="010cb33d-a368-4e4e-bf59-cfbc44ffcb66"
BASE_URL="http://localhost:8888/v1"

# func's to perform curl requests
make_request() {
  local method=$1
  local endpoint=$2
  local data=$3
  local url="$BASE_URL/$endpoint"

  if [ "$method" == "GET" ]; then
    curl -X GET "$url" \
      -H "x-api-key: $API_KEY" \
      -H "x-secret-key: $SECRET_KEY" \
      -H "Content-Type: application/json"
  elif [ "$method" == "POST" ]; then
    curl -X POST "$url" \
      -H "x-api-key: $API_KEY" \
      -H "x-secret-key: $SECRET_KEY" \
      -H "Content-Type: application/json" \
      -d "$data"
  fi
}

# for testing each endpoint
make_request "GET" ""
make_request "GET" "status"
make_request "GET" "currencies"
make_request "GET" "currencies/fiat"
make_request "GET" "currencies/crypto"
make_request "GET" "currencies/BTC"

transaction_data='{
  "from_currency": "EUR",
  "to_currency": "BTC",
  "amount": 100
}'
make_request "POST" "transaction" "$transaction_data"

make_request "GET" "transaction/your_transaction_id"
make_request "GET" "transactions"

make_request "GET" "estimate?from_currency=EUR&to_currency=BTC&amount=100"
make_request "GET" "estimate/by-category"
make_request "GET" "market-info/min-max-range/EUR_BTC"
make_request "GET" "subscriptions"
make_request "GET" "countries"
make_request "GET" "b2b/currencies"
make_request "GET" "b2b/min-max-range/EUR_BTC"

bank_account_data='{
  "payment_category": "SEPA",
  "address": {
    "account_name": "Guardarian",
    "account_number": "XXXXXX000000001387753281",
    "swift": "Swift"
  },
  "intermediary_address": {
    "bank_name": "Bankname",
    "bank_address": "Bank address",
    "bank_country": "ET",
    "swift_bic_number": "Swift"
  }
}'
make_request "POST" "b2b/add-bank-account" "$bank_account_data"

crypto_wallet_data='{
  "currency": "USDT",
  "network": "BSC",
  "wallet_address": "0xd9c844e23cde35aaef5266b0cde66c99d8999999"
}'
make_request "POST" "b2b/add-crypto-wallet" "$crypto_wallet_data"

make_request "GET" "b2b/payout-addresses"
make_request "GET" "b2b/estimate?from_currency=EUR&to_currency=BTC&from_amount=100&from_network=null&to_network=BNB"

b2b_transaction_data='{
  "from_amount": 100,
  "from_currency": "EUR",
  "to_currency": "USDT",
  "from_network": null,
  "to_network": "ETH",
  "payout_account_address": "0x123213123C9b231231230AF21123"
}'
make_request "POST" "b2b/transaction" "$b2b_transaction_data"

make_request "GET" "b2b/transactions?offset=0&limit=50&from_date=2023-01-01&to_date=2023-01-31&sorting=desc"

kyc_data='{
  "first_name": "John",
  "last_name": "Doe",
  "dob": "1990-01-01",
  "country": "US",
  "document_type": "passport",
  "document_number": "123456789"
}'
make_request "POST" "kyc" "$kyc_data"

make_request "GET" "kyc/your_kyc_id"
