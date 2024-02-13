// Sample device data
const devices = [
    { name: 'Device 1', flagged: false, passwordChanged: true, lastPasswordChange: '2024-02-10', ipAddress: '192.168.1.10' },
    { name: 'Device 2', flagged: true, passwordChanged: false, ipAddress: '192.168.1.11' },
    { name: 'Device 3', flagged: false, passwordChanged: true, lastPasswordChange: '2024-02-08', ipAddress: '192.168.1.12' }
];

// Function to display devices
function showDevices() {
    const flaggedDevicesContainer = document.getElementById('flaggedDevices');
    const unflaggedDevicesContainer = document.getElementById('unflaggedDevices');
    flaggedDevicesContainer.innerHTML = '';
    unflaggedDevicesContainer.innerHTML = '';

    devices.forEach(device => {
        const deviceElement = document.createElement('div');
        deviceElement.classList.add('device');
        deviceElement.innerHTML = `
            <div class="deviceHeader">
                ${device.name} (${device.ipAddress})
                <span class="expandIcon">+</span>
            </div>
            <div class="deviceDetails">
                <p>Flagged: ${device.flagged ? 'Yes' : 'No'}</p>
                <p>Password Changed: ${device.passwordChanged ? 'Yes' : 'No'}</p>
                ${device.passwordChanged ? `<p>Last Password Change: ${device.lastPasswordChange}</p>` : ''}
                ${device.flagged ? `<button onclick="changePassword('${device.name}')">Change Password</button>` : ''}
            </div>
        `;

        if (device.flagged) {
            flaggedDevicesContainer.appendChild(deviceElement);
        } else {
            unflaggedDevicesContainer.appendChild(deviceElement);
        }
    });

    // Add event listeners to device headers
    const deviceHeaders = document.querySelectorAll('.deviceHeader');
    deviceHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const details = header.nextElementSibling;
            details.classList.toggle('show');
            const expandIcon = header.querySelector('.expandIcon');
            expandIcon.textContent = details.classList.contains('show') ? '-' : '+';
        });
    });
}


document.addEventListener("DOMContentLoaded", function() {
    const modeToggle = document.getElementById('modeToggle');
    const modeLabel = document.getElementById('toggleLabel');
    const slider = document.getElementById('slider');

    modeToggle.checked = false;
    modeLabel.textContent = 'Monitoring';
    slider.style.backgroundColor = '#4CAF50';
});

// Function to toggle mode
function toggleMode() {
    const modeToggle = document.getElementById('modeToggle');
    const modeLabel = document.getElementById('toggleLabel');
    const slider = document.getElementById('slider');

    if (modeToggle.checked) {
        modeLabel.textContent = 'Active';
        slider.style.backgroundColor = '#FF6347';
    } else {
        modeLabel.textContent = 'Monitoring';
        slider.style.backgroundColor = '#4CAF50';
    }
}


// Function to handle changing password
function changePassword(deviceName) {
    alert(`Password change requested for ${deviceName}`);
}

// Load devices when the page loads
showDevices();

function logout() {
    alert('Logged out successfully!');
    window.location.href = 'login.html'; 
}

document.getElementById('logoutButton').addEventListener('click', logout);
