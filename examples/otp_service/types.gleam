import gleam/option.{type Option}
import gleam/result

pub opaque type SessionToken {
  SessionToken(value: String)
}

pub type UserRole {
  Admin
  Member(team_id: String)
  Guest
}

pub type Account {
  Account(
    id: Int,
    email: String,
    role: UserRole,
    token: Option(SessionToken),
  )
}

pub fn new_account(id: Int, email: String) -> Result(Account, String) {
  case email {
    "" -> Error("Email cannot be blank")
    _ -> Ok(Account(id: id, email: email, role: Member("engineering"), token: option.None))
  }
}
