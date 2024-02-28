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
                    ${device.Password !== '' ? `<p>Password: ${device.Password}</p>` : `
                        <input type="text" placeholder="Enter password" id="passwordInput-${deviceName}">
                        <button class="changePasswordBtn" data-device-name="${deviceName}">Change Password</button>
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
        const deviceName = event.target.dataset.deviceName;
        const passwordInput = document.getElementById(`passwordInput-${deviceName}`);
        const newPassword = passwordInput.value.trim();
        if (newPassword !== '') {
            const updatedDeviceData = {}; // Create an object to hold the updated device data
            updatedDeviceData[deviceName] = { // Include the device name in the object
                password: newPassword,
                PasswordChanged: true
            };
            saveDeviceData(updatedDeviceData);
            passwordInput.disabled = true; // Disable the password input field
            event.target.textContent = 'Reveal Password'; // Change button text to "Reveal Password"
            event.target.classList.remove('changePasswordBtn'); // Remove class to prevent further password changes
            event.target.classList.add('revealPasswordBtn'); // Add new class for revealing password
        }
    } else if (event.target.classList.contains('revealPasswordBtn')) {
        const deviceName = event.target.dataset.deviceName;
        const passwordElement = document.getElementById(`password-${deviceName}`);
        const hashedPassword = passwordElement.dataset.hashedPassword;
        passwordElement.textContent = hashedPassword; // Display hashed password
        event.target.style.display = 'none'; // Hide the "Reveal Password" button
    }
});


function saveDeviceData(data) {
    // Implement saving the updated device data to the server
    fetch('save_passwords.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            console.log("Device data updated successfully");
        } else {
            console.error("Error updating device data");
        }
    })
    .catch(error => {
        console.error("Error updating device data:", error);
    });
}

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
    window.location.href = 'login.html'; 
}

document.getElementById('logoutButton').addEventListener('click', logout);
