sed -i 's/assert_match/raw assert_match/g' tests/test_basic.npk
# Wait, func:assert_match shouldn't be matched
sed -i 's/func:raw assert_match/func:assert_match/g' tests/test_basic.npk
