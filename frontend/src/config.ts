
const urlFromEnv = process.env.REACT_APP_API_URL;
console.log(urlFromEnv)
export const BASE_URL = urlFromEnv === undefined ? 'http://localhost:8000' : urlFromEnv;


const wsConnectionProtocol = BASE_URL.startsWith('https') ? 'wss' : 'ws';

const protocolToReplace = BASE_URL.startsWith('https') ? 'https' : 'http';

export const WS_URL = BASE_URL.replace(protocolToReplace, wsConnectionProtocol) + '/api/v1/ws';

