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

// MySQL DB access module, for use by plugins and others
// For the module that implements interactive DB functionality see mod_db

#ifndef _MOD_CRUD_COLLECTION_MODIFY_H_
#define _MOD_CRUD_COLLECTION_MODIFY_H_

#include "collection_crud_definition.h"

namespace mysh
{
  namespace mysqlx
  {
    class Collection;

    /**
    * Handler for Modify operations on Collections.
    * \todo Document arrayInsert()
    * \todo Document arraydelete()
    * \todo Implement and document bind({var:val, var:val, ...})
    * \todo Update execute to support options and document it
    */
    class CollectionModify : public Collection_crud_definition, public boost::enable_shared_from_this<CollectionModify>
    {
    public:
      CollectionModify(boost::shared_ptr<Collection> owner);
    public:
      virtual std::string class_name() const { return "CollectionModify"; }
      static boost::shared_ptr<shcore::Object_bridge> create(const shcore::Argument_list &args);
      shcore::Value modify(const shcore::Argument_list &args);
      shcore::Value set(const shcore::Argument_list &args);
      shcore::Value unset(const shcore::Argument_list &args);
      shcore::Value merge(const shcore::Argument_list &args);
      shcore::Value array_insert(const shcore::Argument_list &args);
      shcore::Value array_append(const shcore::Argument_list &args);
      shcore::Value array_delete(const shcore::Argument_list &args);
      shcore::Value sort(const shcore::Argument_list &args);
      shcore::Value limit(const shcore::Argument_list &args);
      shcore::Value bind(const shcore::Argument_list &args);

      virtual shcore::Value execute(const shcore::Argument_list &args);
#ifdef DOXYGEN
      CollectionModify modify([String searchCondition]);
      CollectionModify set(Map map);
      CollectionModify unset(string {, string ...});
      CollectionModify array_append(String name, int value);
      CollectionModify array_append(String name, String value);
      CollectionModify array_append(String name, double value);
      CollectionModify array_append(String name, object value);
      CollectionModify sort(List sortExprStr);
      CollectionModify limit(Integer numberOfRows);
      CollectionModify skip(Integer limitOffset);
      CollectionModify bind(Map placeHolderValues);
      Collection_resultset execute(ExecuteOptions opt);
#endif
    private:
      std::auto_ptr< ::mysqlx::ModifyStatement> _modify_statement;
    };
  };
};

#endif
