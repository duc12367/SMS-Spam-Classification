#!/usr/bin/env bash
# Chạy lại toàn bộ pipeline từ dữ liệu thô đến kết quả. Log lưu ở results/logs/.
set -e
cd "$(dirname "$0")"
mkdir -p results/logs results/figures results/tables report/tables report/figures models
if [ ! -f data/SMSSpamCollection ]; then
  echo "Thiếu data/SMSSpamCollection – xem README.md (mục Dữ liệu)"; exit 1
fi
python src/eda.py            2>&1 | tee results/logs/eda.log
python src/experiments.py    2>&1 | tee results/logs/experiments.log
python src/error_analysis.py 2>&1 | tee results/logs/error_analysis.log
python src/make_report_tables.py
cp results/figures/*.png report/figures/
echo "Xong. Biên dịch báo cáo:  cd report && xelatex report.tex && xelatex report.tex"
