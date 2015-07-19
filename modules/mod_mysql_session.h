/*
 * Copyright (c) 2015, Oracle and/or its affiliates. All rights reserved.
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

// Interactive session access module
// Exposed as "session" in the shell

#ifndef _MOD_SESSION_H_
#define _MOD_SESSION_H_

#include "mod_common.h"
#include "shellcore/types.h"
#include "shellcore/types_cpp.h"
#include "shellcore/ishell_core.h"
#include "mysql.h"
#include "base_session.h"

#include <boost/enable_shared_from_this.hpp>

namespace shcore
{
  class Shell_core;
  class Proxy_object;
};

namespace mysh
{
  namespace mysql
  {
    class Schema;
    class MOD_PUBLIC Session : public BaseSession, public boost::enable_shared_from_this<Session>
    {
    public:
      Session();
      virtual ~Session() {};

      // Virtual methods from object bridge
      virtual std::string class_name() const { return "Session"; };
      virtual shcore::Value get_member(const std::string &prop) const;
      std::vector<std::string> get_members() const;

      // Virtual methods from ISession
      virtual shcore::Value connect(const shcore::Argument_list &args);
      virtual shcore::Value close(const shcore::Argument_list &args);
      virtual shcore::Value executeSql(const shcore::Argument_list &args);
      virtual bool is_connected() const { return _conn ? true : false; }

      virtual std::string uri() const;
      virtual shcore::Value get_schema(const shcore::Argument_list &args) const;
      virtual shcore::Value set_default_schema(const shcore::Argument_list &args);

      static boost::shared_ptr<shcore::Object_bridge> create(const shcore::Argument_list &args);

      Connection *connection();

    private:
      void _update_default_schema(const std::string& name);
      void _load_default_schema();
      void _load_schemas();

      boost::shared_ptr<Connection> _conn;

      boost::shared_ptr<Schema> _default_schema;
      boost::shared_ptr<shcore::Value::Map_type> _schemas;

      //boost::shared_ptr<shcore::Proxy_object> _schema_proxy;

      bool _show_warnings;
    };
  };
};

#endif