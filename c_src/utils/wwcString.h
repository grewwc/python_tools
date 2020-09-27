#pragma once

#include <vector>
#include <string>
#include <regex>
#include <functional>

class wwcString : public std::string
{
public:
    wwcString() = default;

    wwcString(std::string &&s) noexcept
        : std::string{move(s)} {};

    wwcString(const std::string &s) noexcept
        : std::string{s} {};

    wwcString(const wwcString &other) noexcept
        : std::string{other} {};

    wwcString(wwcString &&other) noexcept
        : std::string((std::string &&) move(other))
    {
    }

    // not sure if should be explicit
    // if explicit, wwcString not easy to use
    wwcString(const char *s) noexcept
        : std::string{s}
    {
    }

    wwcString &operator=(const wwcString &other) noexcept
    {
        std::string::operator=(other);
        return *this;
    }

    wwcString &operator=(wwcString &&other) noexcept
    {
        std::string::operator=((std::string &&) move(other));
        return *this;
    }

    wwcString &operator=(std::string &&s) noexcept
    {
        std::string::operator=(move(s));
        return *this;
    }

    wwcString &operator=(const std::string &s) noexcept
    {
        std::string::operator=(s);
        return *this;
    }

    wwcString &operator=(const char *s) noexcept
    {
        std::string::operator=(s);
        return *this;
    }

    wwcString &lstrip(char ch = ' ') noexcept;

    wwcString &rstrip(char ch = ' ') noexcept;

    wwcString &strip(char ch = ' ') noexcept;

    wwcString lstrip_copy(char ch = ' ') const noexcept;

    wwcString rstrip_copy(char ch = ' ') const noexcept;

    wwcString strip_copy(char ch = ' ') const noexcept;

    std::vector<wwcString> split(char ch = ' ') const noexcept;

    template <typename Container>
    static wwcString join(const char *delim, Container &&data)
    {
        if (data.size() == 0)
            return wwcString{""};
        std::ostringstream os;
        const auto dilim_len = strlen(delim);
        for (auto &&each_str : std::forward<Container>(data))
        {
            os << each_str << delim;
        }
        auto temp = os.str();
        // remove the last delim
        temp.erase(temp.cend() - dilim_len, temp.cend());
        return wwcString{move(temp)};
    }

    double to_double() const noexcept;
    int to_int() const noexcept;
    long to_long() const noexcept;
    float to_float() const noexcept;

    std::vector<long> find_all_long() const noexcept;
    std::vector<double> find_all_double() const noexcept;
    int find_regex(const std::regex &p) const noexcept;
    std::vector<std::size_t> find_all(const char *data) const noexcept;

    std::size_t count(char ch) const noexcept;

    wwcString toLower_copy() const noexcept;
    wwcString &toLower() noexcept;

    wwcString toUpper_copy() const noexcept;
    wwcString &toUpper() noexcept;

    wwcString toCap_copy() const noexcept;
    wwcString &toCap() noexcept;

    bool startsWith(const std::string &begin) const noexcept;
    bool startsWith(std::string &&begin) const noexcept;
    bool endsWith(const std::string &end) const noexcept;
    bool endsWith(std::string &&end) const noexcept;

    bool startsWith(const wwcString &begin) const noexcept;
    bool startsWith(wwcString &&begin) const noexcept;
    bool endsWith(const wwcString &end) const noexcept;
    bool endsWith(wwcString &&end) const noexcept;

    bool startsWith(const char *begin) const noexcept;
    bool endsWith(const char *end) const noexcept;

    wwcString &replace_char_fn(const std::function<char(char)> &) noexcept;
    wwcString replace_char_fn_copy(const std::function<char(char)> &) const noexcept;

    template <typename T>
    bool contains(T &&arg)
    {
        auto end_it = std::end(arg);
        if constexpr (std::is_same_v<std::decay_t<decltype(arg)>, const char *> || std::is_same_v<std::decay_t<decltype(arg)>, char *>)
        {
            std::advance(end_it, -1);
        }
        auto it = std::search(std::cbegin(*this), std::cend(*this), std::boyer_moore_searcher(std::cbegin(arg), end_it));
        return it != std::cend(*this);
    }

    wwcString operator*(const size_t N) const noexcept;
    friend wwcString operator*(const size_t N, const wwcString &ws);
    void operator*=(const size_t N) noexcept;

    std::vector<wwcString> line_wrap(const size_t N) const noexcept;
};
