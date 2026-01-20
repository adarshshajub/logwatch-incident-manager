<h1>📊 LogWatch Incident Manager</h1>

<p>
  <strong>LogWatch Incident Manager</strong> is a Flask-based log monitoring and alerting system
  designed to ingest logs from file-based sources, monitor them on a schedule, and trigger
  alerts such as <strong>Email notifications</strong> and <strong>ServiceNow incidents</strong>.
</p>

<p>
  This project is inspired by enterprise tools like Splunk and ServiceNow and is built
  as an extensible, role-based alerting platform.
</p>

<hr>

<h2>🚀 Features</h2>

<ul>
  <li>User authentication & role-based access (Admin / User)</li>
  <li>Log ingestion from file paths (JSON & text logs)</li>
  <li>Search logs by keyword</li>
  <li>Configurable alert rules with execution intervals</li>
  <li>Email alerts with HTML support and importance levels</li>
  <li>ServiceNow incident creation (plain-text safe)</li>
  <li>Scheduler-based alert execution</li>
  <li>Alert execution history & audit trail</li>
  <li>Admin management of log sources</li>
</ul>

<hr>

<h2> Project Architecture</h2>

<pre>
logwatch-incident-manager/
│
├── app/
│   ├── __init__.py           # App factory
│   ├── config.py             # Configuration
│   ├── extensions.py         # DB, Login, Migrate
│   │
│   ├── auth/                 # Authentication & users
│   ├── logs/                 # Log ingestion & search
│   ├── alerts/               # Alert rules & actions
│   ├── scheduler.py          # APScheduler jobs
│   │
│   ├── models/               # SQLAlchemy models
│   └── services/             # Email & ServiceNow services
│
├── migrations/               # Alembic migrations
├── instance/app.db           # SQLite database
├── run.py                    # App entry point
└── requirements.txt
</pre>

<hr>

<h2> Roles & Permissions</h2>

<ul>
  <li><strong>Admin</strong>
    <ul>
      <li>Manage log sources</li>
      <li>Manage users</li>
      <li>View all alerts</li>
    </ul>
  </li>
  <li><strong>User</strong>
    <ul>
      <li>Create and manage own alerts</li>
      <li>Search logs</li>
      <li>View alert execution history</li>
    </ul>
  </li>
</ul>

<hr>

<h2>Log Sources</h2>

<p>
  Log sources are defined as file paths. The scheduler periodically reads these files
  and ingests new log entries into the database.
</p>

<ul>
  <li>Supports JSON logs</li>
  <li>Supports plain text logs</li>
  <li>Duplicate ingestion prevention</li>
</ul>

<hr>

<h2> Alert Scheduling</h2>

<p>
  Alerts are executed by an APScheduler background job.
</p>

<ul>
  <li>Each alert has an execution interval (minutes)</li>
  <li>Execution state is tracked in <code>alert_run</code></li>
  <li>History is stored in <code>alert_execution</code></li>
</ul>

<span class="badge">INSERT once, UPDATE forever</span>

<hr>

<h2> Email Alerts</h2>

<ul>
  <li>HTML email support</li>
  <li>Email importance (High / Normal / Low)</li>
  <li>Optional log content inclusion</li>
  <li>SMTP configurable via environment variables</li>
</ul>

<p><strong>Email Importance Headers Used:</strong></p>

<ul>
  <li>Importance</li>
  <li>X-Priority</li>
  <li>X-MSMail-Priority</li>
</ul>

<hr>

<h2> ServiceNow Integration</h2>

<ul>
  <li>Creates incidents via REST API</li>
  <li>HTML stripped before sending to ServiceNow</li>
  <li>Configurable priority & descriptions</li>
</ul>

<p>
  ServiceNow descriptions are always sent as <strong>plain text</strong>
  to avoid rendering issues.
</p>

<hr>

<h2> Database Models</h2>

<ul>
  <li><code>User</code> – Authentication & roles</li>
  <li><code>LogSource</code> – File paths</li>
  <li><code>LogEntry</code> – Ingested logs</li>
  <li><code>AlertConfig</code> – Alert rules</li>
  <li><code>AlertAction</code> – Email / ServiceNow actions</li>
  <li><code>AlertRun</code> – Scheduler state</li>
  <li><code>AlertExecution</code> – Execution history</li>
</ul>

<hr>

<h2> Configuration</h2>

<p>Environment variables required:</p>

<pre>
SECRET_KEY=your-secret
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your@email.com
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=Log Monitor <your@email.com>
SERVICENOW_INSTANCE=instance
SERVICENOW_USER=username
SERVICENOW_PASSWORD=password
</pre>

<hr>

<h2> Running the Application </h2>

<pre>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

flask --app run.py db init
flask --app run.py db migrate -m "initial schema"
flask --app run.py db upgrade
python run.py
</pre>

<hr>

<h2> Alert Execution History</h2>

<ul>
  <li>Every execution is recorded</li>
  <li>SUCCESS / FAILED status</li>
  <li>Error messages preserved</li>
  <li>Immutable audit trail</li>
</ul>

<hr>

<h2> Design Principles</h2>

<ul>
  <li>Config ≠ Execution data</li>
  <li>Scheduler state ≠ Execution history</li>
  <li>HTML for Email, Plain Text for ServiceNow</li>
  <li>Backward-compatible alert configs</li>
</ul>

<hr>

<h2> Future Enhancements</h2>

<ul>
  <li>Slack / Teams alerts</li>
  <li>Alert severity mapping</li>
  <li>Deduplication & suppression</li>
  <li>Time-range search</li>
  <li>Dashboard analytics</li>
</ul>

<hr>

