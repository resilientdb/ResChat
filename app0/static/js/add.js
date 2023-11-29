$(document).ready(function () {
    // Toggle collapse when "Add Friend" button is clicked
    $('#addFriendForm').on('shown.bs.collapse', function () {
        $('#friendNameInput').focus(); // Focus on the friend's name input field when shown
    });

    // Handle "Upload Public Key" button click
    $('#uploadKeyBtn').click(function () {
        // Implement the logic to upload the public key here
        // You can open a file picker or perform any required actions
        // For demonstration purposes, you can display an alert:
        print("hello, this is upload")
        alert('Uploading public key...');
    });

    // Handle "Add" button click
    $('#addFriendSubmitBtn').click(function () {
        // Get the friend's name from the input field
        var friendName = $('#friendNameInput').val();

        // Implement the logic to add the friend using the entered name
        // You can send an AJAX request to the server to add the friend
        // After adding the friend, you can update the friend list

        // For demonstration purposes, display a confirmation alert
        alert('Adding friend: ' + friendName);
    });
});
