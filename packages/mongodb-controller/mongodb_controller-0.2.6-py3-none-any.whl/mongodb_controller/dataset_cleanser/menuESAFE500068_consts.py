COLUMNS_RAW = ['순번', '영업일', '종목코드', '종목명', '통화단위', 'FULL기준가', '기준가', '증감', '과표기준가',
       '증감.1', '비거주자과표기준가', '증감.2', '해외비과세과표기준가', '증감.3', '주식편입비율(%)', '세금구분',
       '세금우대과표기준가', '펀드설정원본액', '펀드순자산총액', '적용법률']

COLUMNS_KOREAN = ['순번', '영업일', '종목코드', '종목명', '통화단위', 'FULL기준가', '기준가', '기준가: 증감', '과표기준가',
       '과표기준가: 증감', '비거주자과표기준가', '비거주자과표기준가: 증감', '해외비과세과표기준가', '해외비과세과표기준가: 증감', '주식편입비율(%)', '세금구분',
       '세금우대과표기준가', '펀드설정원본액', '펀드순자산총액', '적용법률']

COLUMNS_ENGLISH = ['fund_index', 'trading_date', 'code', 'name', 'currency', 'full_price', 'price', 'price_change', 'taxable_price',
       'taxable_price_change', 'nonresident_taxable_price', 'nonresident_taxable_price_change', 'overseas_taxfree_price',
       'overseas_taxfree_price_change', 'stock_ratio', 'tax_type', 'tax_benefit_price', 'fund_principal', 'fund_nav',
       'applicable_law']

MAPPING_COLUMNS_FROM_RAW_TO_KOREAN = {col_raw: col_kor for col_raw, col_kor in zip(COLUMNS_RAW, COLUMNS_KOREAN)}
MAPPING_COLUMNS_FROM_RAW_TO_ENGLISH = {col_raw: col_eng for col_raw, col_eng in zip(COLUMNS_RAW, COLUMNS_ENGLISH)}
MAPPING_COLUMNS_FROM_KOREAN_TO_ENGLISH = {col_kor: col_eng for col_kor, col_eng in zip(COLUMNS_KOREAN, COLUMNS_ENGLISH)}
MAPPING_COLUMNS_FROM_ENGLISH_TO_KOREAN = {col_eng: col_kor for col_eng, col_kor in zip(COLUMNS_ENGLISH, COLUMNS_KOREAN)}