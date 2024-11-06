import React from "react";

const UsersList = ({ users }) => {
  return (
    <div>
      <h1>Other Users</h1>
      <table>
        <thead>
          <td>Invite someone to play!</td>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.username}</td>
              <td>
                <button>Invite</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}; // End UserList variable declaration

export default UsersList; // needs to be exported to be used in other files