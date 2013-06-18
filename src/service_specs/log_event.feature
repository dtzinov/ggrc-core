Feature: Log Javascript client events to syslog
  Background:
    Given service description

  Scenario: HTTP Post of log event
    Given a new "LogEvent" named "logevent"
    And HTTP POST of "logevent" to "/api/log_events"
    Then a "200" status code is received
