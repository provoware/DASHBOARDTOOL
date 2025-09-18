<?php
// Einfache PHP-Datei ("PHP": Skriptsprache) zur Demonstration der Syntaxprüfung.
function dashboard_status_panel(): array {
    return [
        'title' => 'Systemstatus',
        'status' => 'ok',
        'timestamp' => date(DATE_ATOM)
    ];
}
