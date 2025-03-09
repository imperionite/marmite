import React, { lazy } from "react";
import { useQuery } from "@tanstack/react-query";
import { jwtDecode } from "jwt-decode";

// import { jwtAtom } from "../atoms/store";
import { fetchUser, fetchPosts, getAccessToken } from "../services/http";

const Loader = lazy(() => import("./Loader"));

const Dashboard = () => {
  const token = getAccessToken();
  const decoded = jwtDecode(token);
  const userId = decoded?.user_id;

  // Fetch user profile
  const { data: userProfile, isLoading: loadingProfile } = useQuery({
    queryKey: ["userProfile", userId],
    queryFn: async () => fetchUser(userId),
    enabled: !!userId,
  });

  // Fetch posts created by the user
  const { data: posts, isLoading: loadingPosts } = useQuery({
    queryKey: ["posts", userId],
    queryFn: async () => fetchPosts(userId),
    enabled: !!userId,
  });

  if (loadingProfile || loadingPosts) return <Loader />;

  return (
    <div className="container">
      {/* User Profile */}
      <section>
        <h3>User Profile</h3>
        <UserProfileDetails profile={userProfile} />
      </section>

      {/* User Posts */}
      <section>
        <h4>Your Posts</h4>
        <PostsList posts={posts} />
      </section>
    </div>
  );
};

// Extracted components for better readability
const UserProfileDetails = ({ profile }) => (
  <table>
    <tbody>
      <tr data-theme="dark">
        <th>Username:</th>
        <td>{profile?.username}</td>
      </tr>
      <tr>
        <th>Email:</th>
        <td>{profile?.email}</td>
      </tr>
      <tr>
        <th>User ID:</th>
        <td>{profile?.id}</td>
      </tr>
      <tr>
        <th>Date Joined:</th>
        <td>
          {new Date(profile?.created_at).toLocaleString("en-US", {
            dateStyle: "long",
            timeStyle: "short",
          })}
        </td>
      </tr>
    </tbody>
  </table>
);

const PostsList = ({ posts }) =>
  posts.length > 0 ? (
    <table>
      <thead data-theme="dark">
        <tr>
          <th>Post ID</th>
          <th>Content</th>
          <th>Created</th>
        </tr>
      </thead>
      <tbody>
        {posts.map((post) => (
          <tr key={post?.id}>
            <td>{post?.id}</td>
            <td>{post?.content}</td>
            <td>
              {new Date(post?.created_at).toLocaleString("en-US", {
                dateStyle: "long",
                timeStyle: "short",
              })}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  ) : (
    <p>No posts found.</p>
  );
export default Dashboard;
