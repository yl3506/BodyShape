<?php
echo "php started";

$conn = pg_connect(getenv("DATABASE_URL"));

if (!$conn){
    echo "connection failed.";
} else {
    echo "connection succeeded.";
}

$query = "CREATE TABLE IF NOT EXISTS exp3c_pilot4_large3 (
            subject_id VARCHAR(80) PRIMARY KEY,
            data_string TEXT NOT NULL,
            updated_on TIMESTAMP NOT NULL
            );
            INSERT INTO exp3c_pilot4_large3 VALUES ('$_POST[subjectID]','$_POST[dataString]', CURRENT_TIMESTAMP) ON CONFLICT (subject_id) DO UPDATE 
                    SET data_string='$_POST[dataString]', 
                        updated_on=CURRENT_TIMESTAMP;
            ";

$result = pg_query($conn, $query);
if(!$result){
    echo pg_last_error($conn);
} else {
    echo "Records created successfully\n";
}

pg_close($conn);

?>