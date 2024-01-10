export const BASE_URL = 'http://localhost:8000';


const wsConnectionProtocol = BASE_URL.startsWith('https') ? 'wss' : 'ws';

const protocolToReplace = BASE_URL.startsWith('https') ? 'https' : 'http';

export const WS_URL = BASE_URL.replace(protocolToReplace, wsConnectionProtocol) + '/api/v1/dlna/ws';

