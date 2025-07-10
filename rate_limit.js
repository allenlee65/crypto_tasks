import http from 'k6/http';

export const options = {
  scenarios: {
    constant_request_rate: {
      executor: 'constant-arrival-rate',
      rate: 100, // 100 iterations (requests) per second
      timeUnit: '1s', // per second
      duration: '30s', // test duration (adjust as needed)
      preAllocatedVUs: 101  // initial pool of virtual users
      //maxVUs: 200, // maximum VUs if needed
    },
  },
};

export default function () {
  http.get('https://uat-api.3ona.co/exchange/v1/public/get-candlestick?instrument_name=BTC_USDT');
}