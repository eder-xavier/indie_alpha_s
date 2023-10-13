document.addEventListener('DOMContentLoaded', function () {
    const sendFriendRequestButtons = document.querySelectorAll('.send-friend-request-button');

    sendFriendRequestButtons.forEach(button => {
        button.addEventListener('click', function () {
            const userId = button.getAttribute('data-user-id');
            sendFriendRequest(userId);
        });
    });
});

function sendFriendRequest(userId) {
    fetch(`/send_friend_request/${userId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Friend request sent successfully.');
            } else if (data.status === 'error') {
                alert('Friend request already sent.');
            } else {
                alert('An error occurred while sending the friend request.');
            }
        })
        .catch(error => {
            console.error('Error sending friend request:', error);
        });
}
