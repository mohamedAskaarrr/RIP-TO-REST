 // API endpoints
const API_BASE_URL = '/api';
const ROUTERS_ENDPOINT = `${API_BASE_URL}/routers`;

// Authentication token
let authToken = localStorage.getItem('authToken');

// Fetch routers
async function fetchRouters() {
    try {
        const response = await fetch(ROUTERS_ENDPOINT, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const routers = await response.json();
        displayRouters(routers);
    } catch (error) {
        console.error('Error fetching routers:', error);
        showError('Failed to fetch routers');
    }
}

// Display routers in the UI
function displayRouters(routers) {
    const routerList = document.getElementById('routerList');
    routerList.innerHTML = routers.map(router => `
        <div class="router-item mb-3">
            <h6>${router.name}</h6>
            <p>IP: ${router.ip_address}</p>
            <p>Status: <span class="badge ${router.status === 'connected' ? 'bg-success' : 'bg-danger'}">${router.status}</span></p>
            <button class="btn btn-sm btn-primary" onclick="fetchRoutingTable(${router.id})">View Routes</button>
        </div>
    `).join('');
}

// Fetch routing table for a specific router
async function fetchRoutingTable(routerId) {
    try {
        const response = await fetch(`${ROUTERS_ENDPOINT}/${routerId}/routes`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const routes = await response.json();
        displayRoutingTable(routes);
    } catch (error) {
        console.error('Error fetching routing table:', error);
        showError('Failed to fetch routing table');
    }
}

// Display routing table in the UI
function displayRoutingTable(routes) {
    const routingTable = document.getElementById('routingTable');
    routingTable.innerHTML = `
        <table class="table">
            <thead>
                <tr>
                    <th>Destination</th>
                    <th>Next Hop</th>
                    <th>Metric</th>
                </tr>
            </thead>
            <tbody>
                ${routes.map(route => `
                    <tr>
                        <td>${route.destination}</td>
                        <td>${route.next_hop}</td>
                        <td>${route.metric}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

// Show error message
function showError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container').prepend(alertDiv);
}

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', () => {
    fetchRouters();
    // Refresh data every 30 seconds
    setInterval(fetchRouters, 30000);
});