// main_page.js

document.addEventListener("DOMContentLoaded", function() {
    const showDevicesButton = document.getElementById('showDevicesButton');

    showDevicesButton.addEventListener('click', startDevicePopulation);

    const modeToggle = document.getElementById('modeToggle');
    const modeLabel = document.getElementById('toggleLabel');
    const slider = document.getElementById('slider');

    modeToggle.checked = false;
    modeLabel.textContent = 'Monitoring';
    slider.style.backgroundColor = '#4CAF50';
});

async function startDevicePopulation() {
    const progressBar = document.getElementById('progress-bar');
    progressBar.style.display = 'block';
    progressBar.style.width = '0%';

    try {
        await runNetScanScript();
        await showDevices();
    } catch (error) {
        console.error('Error populating devices:', error);
        progressBar.style.display = 'none';
    }
}

async function runNetScanScript() {
    console.log("Trying to run Script")
    try {
        const response = await fetch('run_script.php'); 
        if (!response.ok) {
            console.log("Failed to Run")
            throw new Error('Failed to run netScan.py script');
        }
    } catch (error) {
        throw new Error('Failed to run netScan.py script');
    }
}

async function showDevices() {
    const flaggedDevicesContainer = document.getElementById('flaggedDevices');
    const unflaggedDevicesContainer = document.getElementById('unflaggedDevices');
    const progressBarContainer = document.getElementById('progress-bar-container');
    const progressBar = document.getElementById('progress-bar');

    progressBar.style.width = '0%';

    flaggedDevicesContainer.innerHTML = '';
    unflaggedDevicesContainer.innerHTML = '';

    try {
        const response = await fetch('../Backend_Scripts/localIP.json');
        const devicesData = await response.json();

        let count = 0;
        const totalDevices = Object.keys(devicesData).length;
        const delayBetweenDevices = 1000; // milliseconds

        progressBarContainer.style.display = 'block';

        for (const deviceName in devicesData) {
            const device = devicesData[deviceName];

            const deviceElement = document.createElement('div');
            deviceElement.classList.add('device');
            deviceElement.innerHTML = `
                <div class="deviceHeader" onclick="toggleDeviceDetails(this)">
                    ${deviceName}
                    <span class="expandIcon">+</span>
                </div>
                <div class="deviceDetails">
                    <p>IP: ${device.IP}</p>
                    <p>MAC: ${device.MAC}</p>
                    <p>Company: ${device.Company}</p>
                    <p>Flagged: ${device.flagged ? 'Yes' : 'No'}</p>
                    <p>Password Changed: ${device.passwordChanged ? 'Yes' : 'No'}</p>
                    <p>Device  Accessible: ${device.Accessible ? 'Yes' : 'No'}</p>
                    ${device.passwordChanged ? `<p>Last Password Change: ${device.lastPasswordChange}</p>` : ''}
                    ${device.Accessible ? `<button onclick="changePassword('${deviceName}')">Change Password</button>` : ''}
                </div>
            `;

            // Add a slight delay before appending the device element
            await new Promise(resolve => setTimeout(resolve, delayBetweenDevices));

            if (device.flagged) {
                flaggedDevicesContainer.appendChild(deviceElement);
            } else {
                unflaggedDevicesContainer.appendChild(deviceElement);
            }

            // Update progress bar
            count++;
            const progress = (count / totalDevices) * 100;
            progressBar.style.width = `${progress}%`;
        }

        progressBar.style.display = 'none';
    } catch (error) {
        console.error('Error fetching or parsing device data:', error);
        progressBar.style.display = 'none';
    }
}

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

function toggleDeviceDetails(header) {
    const details = header.nextElementSibling;
    details.classList.toggle('show');
    const expandIcon = header.querySelector('.expandIcon');
    expandIcon.textContent = details.classList.contains('show') ? '-' : '+';
}

// Function to handle changing the password for a device
function changePassword(deviceName) {
    if (confirm(`Are you sure you want to change the password for ${deviceName}?`)) {
        // Send a request to the PHP script to change the password for the flagged device
        fetch('change_password.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ deviceName: deviceName })
        })
        .then(response => {
            if (response.ok) {
                console.log("Password changed successfully");
                // Reload the page to reflect the updated password
                location.reload();
            } else {
                console.error("Error changing password");
            }
        })
        .catch(error => {
            console.error("Error changing password:", error);
        });
    }
    location.reload();
}


function logout() {
    alert('Logged out successfully!');
    window.location.href = 'login.html'; 
}

document.getElementById('logoutButton').addEventListener('click', logout);

function goToPasswordVault() {
    // Make an AJAX request to fetch the latest password vault data
    fetch('password_vault.json')
    .then(response => {
        if (response.ok) {
            return response.json(); // Parse the JSON response
        } else {
            console.warn('password_vault.json not found. Proceeding with an empty vault.');
            return {}; // Return an empty object if the file doesn't exist yet
        }
    })
    .then(passwordVaultData => {
        return fetch('generate_password_vault.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(passwordVaultData)
        });
    })
    .then(response => {
        if (response.ok) {
            console.log("Password vault updated successfully");
            // Redirect to password_vault.html after successful update
            window.location.href = "password_vault.html";
        } else {
            console.error("Error updating password vault");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

