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

#include "collection_crud_definition.h"
#include "mod_mysqlx_expression.h"
#include <sstream>

using namespace mysh::mysqlx;

::mysqlx::DocumentValue Collection_crud_definition::map_document_value(shcore::Value source)
{
  switch (source.type)
  {
    case shcore::Bool:
    case shcore::UInteger:
    case shcore::Integer:
      return ::mysqlx::DocumentValue(source.as_int());
      break;
    case shcore::String:
      return ::mysqlx::DocumentValue(source.as_string());
      break;
    case shcore::Float:
      return ::mysqlx::DocumentValue(source.as_double());
      break;
    case shcore::Object:
    {
                         shcore::Object_bridge_ref object = source.as_object();

                         boost::shared_ptr<Expression> expression = boost::dynamic_pointer_cast<Expression>(object);

                         if (expression)
                         {
                           std::string expr_data = expression->get_data();
                           if (expr_data.empty())
                            return ::mysqlx::DocumentValue(expr_data, true);
                           else
                             throw shcore::Exception::argument_error("Expressions can not be empty.");
                         }
                         else
                         {
                           std::stringstream str;
                           str << "Unsupported value received: " << source.descr() << ".";
                           throw shcore::Exception::argument_error(str.str());
                         }
    }
      break;
    case shcore::Null:
    case shcore::Array:
    case shcore::Map:
    case shcore::MapRef:
    case shcore::Function:
      std::stringstream str;
      str << "Unsupported value received: " << source.descr();
      throw shcore::Exception::argument_error(str.str());
      break;
  }
}