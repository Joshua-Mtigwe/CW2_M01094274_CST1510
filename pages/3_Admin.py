import streamlit as st
from app_model.db import get_connection
from app_model.hashing import hash_generation
from app_model.sidebar import sidebar

sidebar()

st.set_page_config(
    page_title="Admin Panel",
    page_icon="🔐"
)


# Security check
if "logged_in" not in st.session_state:
    st.switch_page("Home.py")


if st.session_state.role != "admin":
    st.error("⛔ Access denied. You are not admin🥸.")
    st.stop()


st.title("🔐 Admin Panel")

st.success(
    f"Welcome Admin {st.session_state.username}"
)

conn = get_connection()

users = conn.execute(
    "SELECT id, username, role, status FROM users"
).fetchall()


st.subheader("👥 User Management")

# Get users
users = conn.execute(
    "SELECT username, role, status FROM users"
).fetchall()

# Convert database result into a table format
user_table = []

for user in users:
    user_table.append({
        "Username": user[0],
        "Role": user[1],
        "Status": user[2]
    })

# Display table
st.dataframe(
    user_table,
    use_container_width=True,
    hide_index=True
)

st.subheader("🚫 Block User")

usernames = [user[0] for user in users]

selected_block_user = st.selectbox(
    "Select user to block",
    usernames
)


if st.button("🚫 Block Selected User"):

    conn.execute(
        """
        UPDATE users
        SET status='blocked'
        WHERE username=?
        """,
        (selected_block_user,)
    )

    conn.commit()

    st.success(
        f"{selected_block_user} has been blocked."
    )

    st.rerun()


st.subheader("🗑 Delete User")

selected_delete_user = st.selectbox(
    "Select user to delete",
    usernames
)


if st.button("🗑 Delete Selected User"):

    # Check the selected user's role
    user_role = conn.execute(
        """
        SELECT role FROM users
        WHERE username=?
        """,
        (selected_delete_user,)
    ).fetchone()

    if user_role[0].lower() == "admin":
        st.error("⛔ Admin accounts cannot be deleted.")

    else:
        conn.execute(
            """
            DELETE FROM users
            WHERE username=?
            """,
            (selected_delete_user,)
        )

        conn.commit()

        st.success(
            f"{selected_delete_user} has been deleted."
        )

        st.rerun()



st.subheader("✅ Unblock User")

# Get blocked users only
blocked_users = conn.execute(
    """
    SELECT username 
    FROM users
    WHERE status='blocked'
    """
).fetchall()

blocked_usernames = [user[0] for user in blocked_users]


if blocked_usernames:

    selected_unblock_user = st.selectbox(
        "Select user to unblock",
        blocked_usernames
    )


    if st.button("✅ Unblock Selected User"):

        conn.execute(
            """
            UPDATE users
            SET status='active'
            WHERE username=?
            """,
            (selected_unblock_user,)
        )

        conn.commit()

        st.success(
            f"{selected_unblock_user} has been unblocked."
        )

        st.rerun()

else:
    st.info("No blocked users found.")