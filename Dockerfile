FROM freqtradeorg/freqtrade:stable

WORKDIR /freqtrade

COPY user_data /freqtrade/user_data

EXPOSE 8080

CMD ["trade", "--config", "/freqtrade/user_data/config.sample.json", "--strategy", "SampleStrategy"]
