#include <bits/stdc++.h>
using namespace std;
using ll = long long;

template<typename T>
class StrHash {
    const static int HASH_CNT = 2;
    constexpr static array<int, 2> B = { 1212549181, 1580098811 };
    constexpr static array<int, 2> P = { 1795636019, 1706613661 };
    static vector<vector<int>> pB;

    int n;
    vector<vector<int>> hs;

public:
    static void init_pB(int n) {
        pB.assign(HASH_CNT, vector<int>(n + 1));
        for (int id = 0;id < HASH_CNT;id++) {
            pB[id][0] = 1;
            for (int i = 1;i <= n;i++)
                pB[id][i] = 1LL * pB[id][i - 1] * B[id] % P[id];
        }
    }

    StrHash() {}
    StrHash(const T &s) { init(s); }

    void init(const T &s) {
        n = s.size() - 1;
        hs.assign(HASH_CNT, vector<int>(n + 1));
        for (int id = 0;id < HASH_CNT;id++)
            for (int i = 1;i <= n;i++)
                hs[id][i] = (1LL * hs[id][i - 1] * B[id] + s[i]) % P[id];
    }

    vector<int> substr(int l, int r) {
        if (l > r || l < 0) return vector<int>(HASH_CNT);
        vector<int> ans(HASH_CNT);
        for (int id = 0;id < HASH_CNT;id++)
            ans[id] = (hs[id][r] - 1LL * hs[id][l - 1] * pB[id][r - l + 1] % P[id] + P[id]) % P[id];
        return ans;
    }
    vector<int> prefix(int x) { return substr(1, x); }
    vector<int> suffix(int x) { return substr(n - x + 1, n); }
    vector<int> rsubstr(int l, int r) { return substr(n - r + 1, n - l + 1); }
};
template<typename T>
vector<vector<int>> StrHash<T>::pB;

bool check(int n, int k, string s) {
    // cout << "Length:" << s.size() - 1 << '\n';
    if (s.size() != n + 1) {
        // cout << "Length wrong!" << '\n';
        return false;
    }

    set<int> st;
    for (int i = 1;i <= n;i++) {
        if (s[i] < 'a' || 'z' < s[i]) {
            // cout << s[i] << " is not lowercase Latin letter!" << '\n';
            return false;
        }
        st.insert(s[i]);
    }
    // cout << "Character type count:" << st.size() << '\n';
    if (st.size() > k) {
        // cout << "Character type count wrong!" << '\n';
        return false;
    }

    set<vector<int>> st2;
    StrHash<string> s_hash(s);
    reverse(s.begin() + 1, s.end());
    StrHash<string> rs_hash(s);
    for (int i = 1;i <= n;i++)
        for (int j = i;j <= n;j++)
            if (s_hash.substr(i, j) == rs_hash.rsubstr(i, j))
                st2.insert(s_hash.substr(i, j));
    // cout << "Count:" << st2.size() << '\n';
    // cout << "Expected count:" << 8 * max(1, (int)log2(n)) << '\n';
    if (st2.size() > 8 * max(1, (int)log2(n))) {
        // cout << "Count wrong!" << '\n';
        return false;
    }
    return true;
}

bool solve(int n, int k, string s) {
    s = "?" + s;
    if (check(n, k, s)) return true;
    return false;
}

#include "testlib.h"

int main(int argc, char *args[]){

    registerTestlibCmd(argc, args);

    
    int T = inf.readInt();

    StrHash<string>::init_pB(5000);
    for (int _=1;_<=T;++_) {
        
        
        int n = inf.readInt(), k = inf.readInt();
        string output = ouf.readString();

        if ( !solve(n,k,output) ) quitf(_wa, "Wrong answer on test %d", _);

    }

    quitf(_ok, "The answer is correct.");
    return 0;
}
