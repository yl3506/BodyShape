<?php
echo "php started";
header('Access-Control-Allow-Origin: *');

if(isset($_POST['dataString'])) {
    echo "posting...";
    $fname = $_POST['subjectID'];
    $file_to_save = $fname. ".txt";
    file_put_contents($file_to_save, $_POST['dataString']);
    echo "Success";
} else {
    echo "Object Not Received";
}
?>