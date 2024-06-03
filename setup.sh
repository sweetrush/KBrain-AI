mkdir -p ~/.streamlit/
mkdir -p ~/output/
mkdir -p ~/output/gemini_out
mkdir -p ~/ai_audio



echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\

[theme]\n\
base=\"dark\"\n\
primaryColor=\"#a5ecaa\"\n\
#backgroundColor=\"#1a1919\"\n\
#secondaryBackgroundColor=\"#5f6164\"\n\
textColor=\"#f9f9fb\"



[connections.gsheets]\n\
spreadsheet = \"https://docs.google.com/spreadsheets/d/1Ibu8-3aMZD9Zp5DXhyXV7udu-8-SMsu6TEiYvGFCXXs\"\n\
worksheet = \"<worksheet-gid-or-folder-id>\"\n\
type = \"service_account\"\n\
project_id = \"logintesting-425221\"\n\
project_key_id = \"18273729d9fe092e65b3334e00182867cc166202\"\n\
private_key = \"\n-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCnpeKSRZf4UNUV\nCuuMFSDmSDdQYS97jFY3QBVUoLXCaPTFTjq43ip+V4D6Lg0VTEdc9EtYIU26BJlz\ncS2R7x7xEquknWipasih0hJ9bOTyoYEQp0Kf5q3yIGMdf8xqqO7Q6R3eW/YJ/Ofi\n3vidCVXU2xGtF9LtvD/Kvn0BVnKvsvvpIbmPVbLVD1RiuOcWscAOprsGK/3mUrVe\nCuZTOp2Bj41lfqGCgsTCNY4PAz2TWx0Rl8wYUBvNXj7t/0fD43tOFLm/K3XxuuJm\n5L9iNGKad6lPeYDGjwitGNMpmg0F4UOnxIJi7ePLR2e3ehxbX9XiS5oM/Rm+nKG5\nECSeDvXHAgMBAAECggEAMkF6IBsYqWmh1sMFRWL4D9BKNKBNmZ3CIqHlQw9CLVtF\nNPh0hgKjfmhA076GUYIiSm05QNwK7t5+Gast2/dwsRfFuH0vaMoIBupwfITuRQXB\nKPra8BA4yMKIs8khwD+QB7Q6LfQnV2snIE1y/bBUuJBLRjZEFtw9y0s7MfF2Q9DJ\ngqV3CyzR8P/cHWPnLslnd317BuvRivXhzKmzo/lauvZQdakTnp+ShNjZzvt0Y9qd\ntvdP1PkwRojLNMjEIkXDWq8wzOMZo5rYZR/g1qi4pj0ZJdktvpiZdY6DfBrdkidZ\n7rAMp42ea4UxgkKvoXKaP+1OZVKLvno0360JJ9/tQQKBgQDXXUrCeQ9gBezTFj46\n3YP8q1gHihBf0pehr/7EMO8sufBfndik6a7wW6O0LeHCJjipzXUII3/5JUvilXqh\nq3F+QMgZoHT96bq1pynJKPfiWR8iD307NrbnMRZjmHliBvX9HOA8TarE30v8Ad8M\nueS1OHWE4/uUPePhh8zxKRCMEQKBgQDHR8FCmrGhGX1/Ho8Y6n36AC8brC4QFcVj\nIjWDw4XcW0wntTqmT93L2NtPLvWaZWhGKNYVL4QL1Ji1xH2MVVoRr8jJw8/zMAzx\n4Hxc8z3QJYqtoDm6wy4142vJuxuXGQU7QeubBZ8yFouUDzOtZ3B/n7RG5ymxsH4f\nDpooG8WcVwKBgQDKladNaDNeUDSGG9ZN6THO7B7SeL0OZjrcjYFJa/6QRBgo2YKB\nHpDA6HMFemNzDiEfGXWNQlePNdY8PgAtM+h+qtGPybBDaSmI1sYnw7Hp6YuvroJO\nwRksQLCe3z7PR1z9y7vi/ew1ZRdE5z256uOI1KM3bn2o5M8Hx4axE7/NAQKBgE/z\n9A/67MWL6pPz+MmwWzbQmBXsMNb3RSiO8xWYfr54SserqIpNhNlieir81kFJ6lor\nzCjX1YzBkTtsSErje62Y72A0FdymLKtmu763QNegGFGs9Tx/Tq0EP5zCW0F2Imkx\n+4tI6CQ6c2nF55/s3m/17Wh9GndWLmPbgfIRomklAoGAaxaHu19wqy5mJJS9gttH\nvyNBnJpMde3FppYtQ518Owz0Etk5l22CJ4P8F2xbaQ1XY4N2xlSf5o4N0pjhGVcw\nmQggTvkRtPjZBg+W+qCDIOZOQeEFut9twSUKY3J2j4xVBSxv1nDuigIk+mVi071n\nJHODND1R5Ozv6xBCvc+Q32E=\n-----END PRIVATE KEY-----\n\"\n\
client_email = \"linshtwtr@logintesting-425221.iam.gserviceaccount.com\"\n\
client_id = \"110464953163885343190\"\n\
auth_url = \"https://accounts.google.com/o/oauth2/auth\"\n\
token_uri = \"https://oauth2.googleapis.com/token\"\n\
auth_provider_x509_cert_url = \"https://www.googleapis.com/oauth2/v1/certs\"\n\
client_x509_cert_url = \"https://www.googleapis.com/robot/v1/metadata/x509/linshtwtr%40logintesting-425221.iam.gserviceaccount.com\"\n\


" > ~/.streamlit/config.toml