<?php
include 'config.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $passwd = $_POST['passwd'];
    $response = $_POST['cf-turnstile-response'];
    if ($passwd === '' || $response === '') {
        die('Pls verify captcha or input password');
    }
    $ch = curl_init($SITE_VERIFY);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, [
        'secret' => $SECRET_KEY,
        'response' => $response
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $data = curl_exec($ch);
    curl_close($ch);
    $data = json_decode($data);
    $now = time();
    $challenge_ts = strtotime($data->challenge_ts);
    if ($data->success == 1 && $now - $challenge_ts <= 5) {
        if ($passwd === $PASSWD) {
            die($FLAG);
        } else {
            die('Wrong password!');
        }
    } else {
        die('Verify captcha failed!');
    }
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
    <title>KCSC CTF 2023</title>
</head>

<body>
    <div class="container">
        <section>
            <form action="<?php echo $_SERVER["PHP_SELF"]; ?>" method="POST">
                <h2 class="text-center">KCSC CTF 2023</h2>
                <label for="passwd" class="form-label">Password to unlock the flag:</label>
                <input type="password" name="passwd" class="form-control" id="passwd" placeholder="Input here..."
                    required>
                <br>
                <div class="cf-turnstile" data-sitekey="<?php echo $SITE_KEY; ?>"></div>
                <div class="d-grid gap-2">
                    <button type="submit" class="btn btn-danger">Danger</button>
                </div>
            </form>
        </section>
    </div>
</body>

</html>