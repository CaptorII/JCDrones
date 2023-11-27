    document.addEventListener('DOMContentLoaded', function() {
    // Function to update dashboard after adding a drone
    function updateDashboard() {
        fetch('/drones/get_swarm/')
        .then(response => response.json())
        .then(data => {
            if (data.swarm) {
                document.getElementById('dashboardContent').innerHTML = `
                    <h2>Dashboard</h2>
                    <h3>Swarm Name: ${data.swarm.swarm_name}</h3>
                    <button id="addDroneBtn">Add Drone</button>
                `;
                document.getElementById('addDroneBtn').addEventListener('click', function() {
                    fetch('/drones/add_drone/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': '{{ csrf_token }}'
                        },
                        body: JSON.stringify({
                            swarm_id: data.swarm.swarm_id
                        })
                    })
                    .then(response => {
                        if (response.ok) {
                            console.log('Drone added successfully');
                            updateDashboard();
                        } else {
                            console.error('Error adding drone');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    document.getElementById('addSwarmBtn').addEventListener('click', function() {
        fetch('/drones/add_swarm/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({})
        })
        .then(response => {
            if (response.ok) {
                // Update dashboard on successful swarm creation
                console.log('Swarm added successfully');
                updateDashboard();
            } else {
                console.error('Error adding swarm');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});