async function showDevices() {
    const flaggedDevicesContainer = document.getElementById('flaggedDevices');
    const unflaggedDevicesContainer = document.getElementById('unflaggedDevices');

    flaggedDevicesContainer.innerHTML = '';
    unflaggedDevicesContainer.innerHTML = '';

    try {
        const response = await fetch('password_vault.json'); // Fetch device data from the server
        const devicesData = await response.json();

        for (const deviceName in devicesData) {
            const device = devicesData[deviceName];
            console.log("Hello" + deviceName);

            const deviceElement = document.createElement('div');
            deviceElement.classList.add('device');
            deviceElement.innerHTML = `
                <div class="deviceHeader" onclick="toggleDeviceDetails(this)">
                    ${deviceName}
                    <span class="expandIcon">+</span>
                </div>
                <div class="deviceDetails">
                    <p>Company: ${device.Company}</p>
                    <p>User: ${device.Username}</p>
                    <p>Default Password: ${device.defaultPassword}</p>
                    ${device.Password !== '' ? `
                        <div id="password-${deviceName}-container">
                            <p>Password: 
                                <span id="password-${deviceName}-hidden">${'*'.repeat(device.Password.length)}</span>
                                <span id="password-${deviceName}-reveal" style="display: none">${device.Password}</span>
                                <button class="revealPasswordBtn" data-device-name="${deviceName}">
                                    <i class="bi bi-eye-slash" style="font-size: 1rem;"></i>
                                </button>
                            </p>
                        </div>
                        ` : `
                            <input type="password" placeholder="Enter your current password" id="passwordInput-${deviceName}">
                            <button class="changePasswordBtn" data-device-name="${deviceName}" data-device-mac="${device.MAC}" data-device-IP="${device.IP}">Change Password</button>
                    `}
            </div>
            `;

            if (device.flagged) {
                flaggedDevicesContainer.appendChild(deviceElement);
            } else {
                unflaggedDevicesContainer.appendChild(deviceElement);
            }
        }
    } catch (error) {
        console.error('Error fetching or parsing device data:', error);
    }
    flaggedDevicesContainer.addEventListener('click', toggleDeviceDetails);
    unflaggedDevicesContainer.addEventListener('click', toggleDeviceDetails);
}


document.addEventListener('click', function(event) {
    if (event.target.classList.contains('changePasswordBtn')) {
        // Handle change password button click
        const deviceName = event.target.dataset.deviceName;
        const deviceMAC = event.target.dataset.deviceMac;
        const passwordInput = document.getElementById(`passwordInput-${deviceName}`);
        const newPassword = passwordInput.value.trim();
        const deviceIP = event.target.dataset.deviceIp;

        
        if (newPassword !== '') {
            // Send password change request
            fetch('change_password.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    MAC: deviceMAC,
                    password: newPassword,
                    IP: deviceIP
                })
            })
            .then(() => {
                // Password change request sent, reload the page
                alert('Password change request sent successfully!');

                location.reload();

            })
            .catch(error => {
                console.error('Error changing password:', error);
                alert('Error changing password. Please try again.');
            });
        }
    } else if (event.target.classList.contains('revealPasswordBtn') || event.target.parentElement.classList.contains('revealPasswordBtn')) {
        // Check if the click target is the button or its parent (which might be the icon)
        const button = event.target.classList.contains('revealPasswordBtn') ? event.target : event.target.parentElement;
        const deviceName = button.dataset.deviceName;
        const passwordHidden = document.getElementById(`password-${deviceName}-hidden`);
        const passwordReveal = document.getElementById(`password-${deviceName}-reveal`);
        const revealButtonIcon = button.querySelector('i.bi');

        if (passwordHidden.style.display === 'none' || passwordHidden.style.display === '') {
            // Password is hidden, reveal it
            passwordHidden.style.display = 'inline';
            passwordReveal.style.display = 'none';
            revealButtonIcon.classList.remove('bi-eye');
            revealButtonIcon.classList.add('bi-eye-slash');
        } else {
            // Password is revealed, hide it
            passwordHidden.style.display = 'none';
            passwordReveal.style.display = 'inline-block';
            revealButtonIcon.classList.remove('bi-eye-slash');
            revealButtonIcon.classList.add('bi-eye');
        }
    }
});

function toggleDeviceDetails(event) {
    const deviceHeader = event.target.closest('.deviceHeader');
    if (!deviceHeader) return; // If clicked element is not a device header, exit function
    const expandIcon = deviceHeader.querySelector('.expandIcon');
    const deviceDetails = deviceHeader.nextElementSibling;

    if (expandIcon.textContent === '+') {
        expandIcon.textContent = '-';
        deviceDetails.style.display = 'block';
    } else {
        expandIcon.textContent = '+';
        deviceDetails.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    showDevices();
    // Add event listener for the back button
    const backButton = document.getElementById('backButton');
    backButton.addEventListener('click', function() {
        window.location.href = 'main_page.html'; // Redirect to main_page.html
    });
});

function logout() {
    alert('Logged out successfully!');
    localStorage.removeItem('infoDisplayed');
    window.location.href = 'login.html'; 
}
function loadPasswordVault() {
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
}
window.addEventListener('load', function() {
    loadPasswordVault();
});

document.getElementById('logoutButton').addEventListener('click', logout);
