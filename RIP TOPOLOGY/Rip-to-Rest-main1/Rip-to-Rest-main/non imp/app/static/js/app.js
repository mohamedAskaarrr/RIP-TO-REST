// static/js/app.js
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const loginBtn = document.getElementById('login-btn');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const tokenDisplay = document.getElementById('token-display');
    const routerSection = document.getElementById('router-section');
    const routerSelect = document.getElementById('router-select');
    const getRipDbBtn = document.getElementById('get-rip-db');
    const getRipStatusBtn = document.getElementById('get-rip-status');
    const resultOutput = document.getElementById('result-output');
    
    let token = null;
    
    // Load routers
    function loadRouters() {
        // This would normally come from an API call
        // For demo purposes, we're hardcoding router IDs
        const routers = ['router1', 'router2', 'router3'];
        
        routers.forEach(router => {
            const option = document.createElement('option');
            option.value = router;
            option.textContent = router;
            routerSelect.appendChild(option);
        });
    }
    
    loadRouters();
    
    // Event Listeners
    loginBtn.addEventListener('click', async () => {
        const username = usernameInput.value;
        const password = passwordInput.value;
        
        if (!username || !password) {
            alert('Please enter both username and password');
            return;
        }
        
        try {
            const response = await axios.post('/api/v1/token', {
                username,
                password
            });
            
            token = response.data.access_token;
            tokenDisplay.classList.remove('hidden');
            routerSection.classList.remove('hidden');
            
            // Configure axios defaults for future requests
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            
        } catch (error) {
            alert('Authentication failed: ' + (error.response?.data?.error || error.message));
        }
    });
    
    getRipDbBtn.addEventListener('click', async () => {
        if (!token) {
            alert('Please authenticate first');
            return;
        }
        
        const routerId = routerSelect.value;
        let url = '/api/v1/rip/database';
        
        if (routerId !== 'all') {
            url += `/${routerId}`;
        }
        
        try {
            const response = await axios.get(url);
            resultOutput.textContent = JSON.stringify(response.data, null, 2);
        } catch (error) {
            resultOutput.textContent = 'Error: ' + (error.response?.data?.error || error.message);
        }
    });
    
    getRipStatusBtn.addEventListener('click', async () => {
        if (!token) {
            alert('Please authenticate first');
            return;
        }
        
        const routerId = routerSelect.value;
        let url = '/api/v1/rip/status';
        
        if (routerId !== 'all') {
            url += `/${routerId}`;
        }
        
        try {
            const response = await axios.get(url);
            resultOutput.textContent = JSON.stringify(response.data, null, 2);
        } catch (error) {
            resultOutput.textContent = 'Error: ' + (error.response?.data?.error || error.message);
        }
    });
});