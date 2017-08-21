/*
 * Copyright (c) 2015, 2017, Oracle and/or its affiliates. All rights reserved.
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

#ifndef _ISHELL_CORE_
#define _ISHELL_CORE_

#include <iostream>
#include <vector>
#include <functional>

#include "scripting/object_registry.h"
#include "scripting/types_common.h"
#include "scripting/types.h"
#include "scripting/lang_base.h"
#include "mysqlshdk/libs/utils/enumset.h"

namespace mysqlsh {
// The session types that can be produced by connect_session
enum class SessionType {
  Auto,
  X,
  Node,
  Classic
};
class ShellBaseSession;
};

namespace shcore {

class SHCORE_PUBLIC IShell_core {
 public:
  enum class Mode {
    None = 0,
    SQL = 1,
    JavaScript = 2,
    Python = 3
  };
  typedef shcore::utils::Enum_set<Mode, Mode::Python> Mode_mask;

  static Mode_mask all_scripting_modes() {
    return Mode_mask(Mode::JavaScript).set(Mode::Python);
  }

  IShell_core(void);
  virtual ~IShell_core();

  virtual Mode interactive_mode() const = 0;
  virtual bool switch_mode(Mode mode, bool &lang_initialized) = 0;

  // By default, globals apply to the three languages
  virtual void set_global(const std::string &name, const Value &value,
                          Mode_mask mode = Mode_mask::any()) = 0;
  virtual Value get_global(const std::string &name) = 0;

  virtual Object_registry *registry() = 0;
  virtual void handle_input(std::string &code, Input_state &state, std::function<void(shcore::Value)> result_processor) = 0;
  virtual bool handle_shell_command(const std::string &code) = 0;
  virtual std::string get_handled_input() = 0;
  virtual int process_stream(std::istream& stream, const std::string& source,
      std::function<void(shcore::Value)> result_processor,
      const std::vector<std::string> &argv) = 0;

  // Development Session Handling
  virtual std::shared_ptr<mysqlsh::ShellBaseSession> set_dev_session(const std::shared_ptr<mysqlsh::ShellBaseSession>& session) = 0;
  virtual std::shared_ptr<mysqlsh::ShellBaseSession> get_dev_session() = 0;

  virtual Interpreter_delegate *get_delegate() = 0;

  virtual void print(const std::string &s) = 0;
  virtual void print_error(const std::string &s) = 0;
  virtual bool password(const std::string &s, std::string &ret_pass) = 0;
  virtual const std::string& get_input_source() = 0;
  virtual const std::vector<std::string>& get_input_args() = 0;
  virtual bool print_help(const std::string& topic) = 0;
};
};

#endif