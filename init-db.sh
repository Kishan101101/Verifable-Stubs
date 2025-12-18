#!/bin/bash
set -e

# This script runs after PostgreSQL initialization
# Update pg_hba.conf to accept password connections

echo "host    all             all             0.0.0.0/0               scram-sha-256" >> /var/lib/postgresql/data/pg_hba.conf
echo "host    all             all             ::/0                    scram-sha-256" >> /var/lib/postgresql/data/pg_hba.conf
