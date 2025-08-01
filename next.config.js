/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/tequmsa-internet-field',
        destination: '/api/tequmsaInternetField',
      },
    ];
  },
};

module.exports = nextConfig;