#!/bin/sh

locale-gen en_US en_US.UTF-8

apt-get -y install openssl ssl-cert ca-certificates prosody
pip install sleekxmpp

mkdir -p /var/run/prosody
chown -R prosody.prosody /var/run/prosody

mkdir -p /var/lib/prosody/xmpp%2ememoryoftheworld%2eorg/accounts/
chown -R prosody.prosody /var/lib/prosody
