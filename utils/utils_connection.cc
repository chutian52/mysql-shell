/*
* Copyright (c) 2014, 2017, Oracle and/or its affiliates. All rights reserved.
*
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License as
* published by the Free Software Foundation; version 2 of the
* License.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
* 02110-1301  USA
*/

#include "utils_connection.h"

using namespace shcore;

struct MapSslModeNameToValue::Maps MapSslModeNameToValue::_maps;
std::string MapSslModeNameToValue::_empty = "";


SslInfo::SslInfo(const SslInfo& s) : skip(s.skip), mode(s.mode), ca(s.ca), capath(s.capath),
    crl(s.crl), crlpath(s.crlpath), ciphers(s.ciphers), tls_version(s.tls_version),
    cert(s.cert), key(s.key)
{}