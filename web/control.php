<?php
if (!empty($_GET)) {
  $state = $_GET['state'];
  $duration = $_GET['duration'];
  $unit = $_GET['unit'];
  echo $unit;
  if ($state == "auto") {
    exec('sudo -u klima /opt/klima/bin/fanctl.py unlock');
  } elseif (($state == "on") or ($state == "off")) {
    if ($unit <> "inf") {
      $unit = strval(intval($duration)*intval($unit));
    }
    if ($unit <> "0") {
      exec('sudo -u klima /opt/klima/bin/fanctl.py lock ' . $state . ' ' . $unit);
    }
  }
  header('Location: control.php');
}
?>
<html>
<head>
<title>Keller&uuml;berwachung</title>
<link rel="stylesheet" href="klima.css">
</head>
<body>
<iframe id="sidebar" src="../graphics/sidebar.html"></iframe>
<center>
<h1>Steuerung</h1>
<?php
$lockfile = '/opt/klima/fanctl.lock';

if (file_exists($lockfile)) {
  $duration =  file_get_contents($lockfile);
  if ($duration=="inf") {
    echo 'L&uuml;fter ist <font color="red">dauerhaft gesperrt</font>.';
  } else {
    setlocale (LC_ALL, 'de_DE');
    echo 'L&uuml;fter ist <font color="red">gesperrt bis ';
    echo strftime('%A, %-d.%-m.%Y, %-H:%M', intval($duration));
    echo '</font>.';
  }
} else {
  echo 'L&uuml;fter l&auml;uft im <font color="blue">Automatikbetrieb</font>.';
}
?>
<br>
<br>
<form action="control.php">
L&uuml;fter f&uuml;r
<input type="number" min="0" value="2" name="duration" size="4" style="text-align:right;"><br>
<input type="radio" id="m" name="unit" value="1"><label for="m">Minuten</label>
<input type="radio" id="h" name="unit" value="60" checked="checked"><label for="h">Stunden</label>
<input type="radio" id="d" name="unit" value="1440"><label for="d">Tage</label>
<input type="radio" id="w" name="unit" value="10080"><label for="w">Wochen</label><br>
<input type="radio" id="inf" name="unit" value="inf"><label for="inf">dauerhaft</label><br>
<button type="submit" id="on" name="state" value="on">Einschalten</button>
<button type="submit" id="off" name="state" value="off">Ausschalten</button><br>
<br>
<button type="submit" id="auto" name="state" value="auto">L&uuml;fter auf Automatik schalten</button><br>
</center>
</form>
</body>
